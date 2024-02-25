/*
doc_start&&&/
@category Frontend Component
@file graphFuncs.js
@description 

*/
import { COLORS, ICONCOLORS, PAGECOLORS, makeOpaque } from "../Assets/colors.js";
import { branchNumToColor, bubbleXCoords } from "./graphConstants.js";
import fetchJSONData from "./fetchJSON.js";
const RADIUS = 10;
const textX = 220;
const MAINBRANCH = "main";

// list of all existing branches on visualization
const currBranchSet = new Set();

// map of all branch names to objects containing relevant visualizing properties
const branchNameToProperties = {};

function processBranch(branch) {
    // save index then add branch to set
    const branchIndex = currBranchSet.size;
    currBranchSet.add(branch);

    // initialize then populate properties of new branch
    const branchProperties = {};
    branchProperties.color = branchNumToColor[branchIndex];
    branchProperties.x = bubbleXCoords[branchIndex];
    branchProperties.prevY = -1;

    // cache properties in local variable
    branchNameToProperties[branch] = branchProperties;
    return branchProperties;
}

function processBranchMerge(branch) {
    currBranchSet.delete(branch);
    delete branchNameToProperties[branch];
}

function drawCommitText(x, y, text, ctx) {
    if (text.length > 31) {
        text = text.substring(0, 30) + " ..."
    }

    ctx.font = '12px Arial';
    ctx.fillStyle = PAGECOLORS.whiteText;
    ctx.fillText(text, x, y);
}

function drawCommitBubble(x, y, user, color, ctx) {
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc(x, y, RADIUS, 0, Math.PI * 2, true);
    ctx.fill();
}

function drawCommitLine(branchX, prevY, currY, color, ctx) {
    if (prevY !== -1) {
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.moveTo(branchX, prevY);
        ctx.lineTo(branchX, currY);
        ctx.stroke();
    }
    return;
}

function drawCommitRectangle(x, y, color, ctx) {
    const endX = textX - 5 - x;
    ctx.beginPath();
    ctx.fillStyle = makeOpaque(color);
    ctx.fillRect(x, y - RADIUS, endX, 2 * RADIUS, true);
    ctx.stroke();

    ctx.fillStyle = color;
    ctx.fillRect(textX - 5, y-RADIUS, 2, 2 * RADIUS, true)
    ctx.stroke();
}

function drawArc(startX, startY, endX, endY, color, ctx) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.moveTo(startX, startY);
    
    if (endY < startY) {
        ctx.lineTo(startX, endY + RADIUS);

        ctx.moveTo(endX, endY);
        if (startX < endX) {
            ctx.lineTo(startX + RADIUS, endY);
    
            ctx.arc(startX + RADIUS, endY + RADIUS, RADIUS, 1.5 * Math.PI, Math.PI, true);
        } else {
            ctx.lineTo(startX - RADIUS, endY);

            ctx.moveTo(startX, endY + RADIUS);
            ctx.arc(startX - RADIUS, endY + RADIUS, RADIUS, 0, 1.5 * Math.PI, true);
            
        }
    } else {
        ctx.lineTo(startX, endY - RADIUS);

        if (startX < endX) {
            ctx.moveTo(endX - RADIUS, endY);
            ctx.lineTo(startX + RADIUS, endY);
            ctx.moveTo(startX, endY - RADIUS)
            ctx.arc(startX + RADIUS, endY - RADIUS, RADIUS, 1 * Math.PI, 0.5 * Math.PI, true);
        } else {
            ctx.moveTo(endX + RADIUS, endY);
            ctx.lineTo(startX - RADIUS, endY);

            ctx.moveTo(startX - RADIUS, endY);
            ctx.arc(startX - RADIUS, endY - RADIUS, RADIUS, 0.5 * Math.PI, 0, true);
        }
    }
    

    ctx.stroke();
    
}
function drawCommitArc(endX, endY, branchToMerge, ctx) {
    const mergeBranchParameters = branchNameToProperties[branchToMerge];
    drawArc(mergeBranchParameters.x, mergeBranchParameters.prevY, endX, endY, mergeBranchParameters.color, ctx);
}

function drawCheckoutArc(startX, startY, mainBranch, color, ctx) {
    const mainBranchParameters = branchNameToProperties[MAINBRANCH];
    drawArc(startX, startY, mainBranchParameters.x, mainBranchParameters.prevY, color, ctx)
}

function drawImage(x, y, url, ctx) {
    const base_image = new Image();
    base_image.src = url;
    base_image.onload = () => {
        // Create a circular clipping path
        ctx.beginPath();
        ctx.arc(x, y, 9, 0, Math.PI * 2);
        ctx.closePath();
        ctx.clip();
        
        // Draw the scaled-down image
        ctx.drawImage(base_image, x - 9, y - 9, 18, 18); // Center the image within the circle
    }
}

// width: 100, height = 500
async function drawCommitGraph() {
    try {
        const commits = await fetchJSONData();
        console.log(commits);

        // alert("aaaaaaaaaa")
        const canvas = document.getElementById("graph-canvas");
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = PAGECOLORS.calloutGray;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.textBaseline = 'middle';

        let rowY = 800;

        // if needed: sort the commits based on timestamps
        for (let i = 0; i < commits.length; i++) {
            // grab current commit along with relevant properties
            const currCommit = commits[i];
            const isNewBranch = !currBranchSet.has(currCommit.branch);
            const isMergeCommit = currCommit.mergeInto.length != 0;
            console.log("--------------------------------------------")
            console.log(currCommit);

            let branchProperties = branchNameToProperties[isMergeCommit ? currCommit.mergeInto : currCommit.branch];
            if (isNewBranch) {
                branchProperties = processBranch(currCommit.branch);
                if (currBranchSet.size !== 1) {
                    drawCheckoutArc(branchProperties.x, rowY, MAINBRANCH, branchProperties.color, ctx)
                }
            }

            console.log(currCommit.branch + "-> " + branchProperties);
            // draw commit graph row (text, bubble, line, and box)
            if (isMergeCommit) {
                console.log("is merge commit");
                drawCommitArc(branchProperties.x, rowY,  currCommit.branch, ctx);
                processBranchMerge(currCommit.branch);
            }
            drawCommitText(textX, rowY, currCommit.message, ctx);
            drawCommitBubble(branchProperties.x, rowY, currCommit.user, branchProperties.color, ctx);
            drawCommitLine(branchProperties.x, branchProperties.prevY, rowY, branchProperties.color, ctx);
            drawCommitRectangle(branchProperties.x, rowY, branchProperties.color, ctx);
            // drawImage(branchProperties.x, rowY, url, ctx);
            // decrement y values
            branchProperties.prevY = rowY;
            branchProperties[currCommit.branch] = branchProperties;
            rowY -= 30;
    }
    } catch (error) {
        console.log(error);
    }
    

}





drawCommitGraph();