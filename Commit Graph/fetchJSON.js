// Define the path to the JSON file
export default async function fetchJSONData() {
    try {
        const response = await fetch('../demofile.json');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Unable to fetch data:", error);
        throw error; // Rethrow the error to handle it elsewhere if needed
    }
}