# GitNotate-HackIllinois-2024
## Inspiration
Writing documentation and tracking revision histories is tedious and time-consuming. We wanted to create a tool that parses documentation and automatically generates headers to better organize files. We also wanted to visualize Git branches and commit history to help ease collaboration and debugging.

## What it does
It takes a GitHub repository and creates a Notion page with 2 major widgets:
1) Generates a graphical display that shows all Git branch histories, including merges, checkouts, and commit messages.
2) Populates a database with documentation information for all files. This includes file category, file name, contributors, and file summary. If documentation is not included in any file, we have AI automatically generate a documentation and populate it in the Notion database.
It automatically updates both widgets every time something is comitted to the repository.

## How we built it
We used GitHub API and Notion API to get Git commit information, including documentation and comments, and populate it in a Notion page. For the graph, we used JavaScript to create a display and embed it on the Notion page, taking in a JSON file with all of the commit information.

## Challenges we ran into
**Deploying code:**
We were able to write code and test it locally without too much resistance. Actually having the code run on any computer was challenging. We eventually used Google Cloud Functions to store the function to populate the summary widget, which took a long time to learn and execute, since none of us have much experience with cloud functions.

**Integrating with GitHub Actions:**
To have documentation and the graph be generated on each commit, we needed to program various GitHub actions with .yml extensions. Using .yml was challenging, and trying to give the git bot permissions took the longest time. We had to try various methods, including creating PATs and SSHs. 

## Accomplishments that we're proud of
**Github Actions:** We managed to create a sleek Github Actions script that would run a python file to read the repository, then update a branch on our repository that contains the gh-pages deployment, which was a super cool solution to the problem of integrating the frontend with our backend scripts.

**API usage:** We didn't have much experience with APIs previously, so working with the GitHub REST API and OpenAI were great accomplishments for us. 

**The entire process:** All of us have never created a project for a hackathon before, so starting the process from the beginning, where we were just brainstorming ideas, to fleshing out said ideas, creating mockups, and then actually writing and debugging the code, all while learning how to use APIs and cloud services that we have had no experiences with, was something that we are very proud of. Doing all of that and being able to create a front-end that we were pretty happy with is another accomplishment we are proud of.

## What we learned
**Github Actions**
We learned the basics of how to use Github Actions to help elevate Github workflows. Reading documentation and adapting workflows other individuals have created to assist us gave us a great introduction to writing yml files and helped us learn about the limitations and possibilities of Github Actions.

## What's next for GitNotate
**Notion Widgets**
We have only scratched the surface of what is possible with integrations between Notion and Github. There are essentially infinite possibilities for Notion widgets utilizing the power of Github Pages for ease of deployment, and possibly even more crafty ways to utilize Github Actions to help run these widgets on a completely static website.

The Notion API itself also allows for so many more interactions with different built in widgets and components, and the bounds for additions and integrations are limitless.
