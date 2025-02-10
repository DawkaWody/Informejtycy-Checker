async function submission() {
    const response = await fetch("/submit", {
            method: "POST",
            headers: {
                "content-type": "text/plain",
                "Problem": "0"
            },
            body: `
#include<iostream>
using namespace std;
int main()
{
cout << 15 << endl;
}
        `
    });
    const data = response.json();
    console.log(data);
}

document.getElementById("submissionButton").addEventListener("click", () => {
    submission();
});
