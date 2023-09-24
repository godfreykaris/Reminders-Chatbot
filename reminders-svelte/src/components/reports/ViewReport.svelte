<script>
    
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import { push } from 'svelte-spa-router';
    import { Listgroup } from 'flowbite-svelte';
    
    import {PDFDocument, StandardFonts, rgb} from 'pdf-lib';

    let isLoading = false;

    // @ts-ignore
    let user_data = null;
    let goals = [];

    let selected_goal = null;

    let error_message = '';
    let success_message = '';
    let document_name = '';

    let pdfDataUri = null;

    let headers = new Headers();

    headers.append('Accept', 'application/json');
    // @ts-ignore
    let csrf = document.getElementsByName("csrf-token")[0].content;
    headers.append("X-CSRFToken", csrf);

    const myInit = {
      method: "GET",
      credentials: "same-origin",
      headers: headers,
    };

    async function fetchGoals() {

        isLoading = true;

        // @ts-ignore
        const response = await fetch('/api/get_goals', myInit);

        if (response.status === 200) 
        {
          goals = await response.json();
          isLoading = false;
        } 
        else if (response.status === 401)
        {
          // Redirect to the login page when Unauthorized (401) status is received
          push('/login'); 
        } 
        else {
          error_message = "An error occurred trying to fetch goals";
          success_message = '';
          isLoading = false;
          location.reload();
        }
    }

    fetchGoals();

    async function select_goal(goal){
        selected_goal = goal;
        await FetchReport();
    }

    // Define a function to generate the PDF document
    async function generatePDF(reportText, selectedGoal) {
    
      isLoading = true;

      const pdfDoc = await PDFDocument.create();
      const timesRomanFont = await pdfDoc.embedFont(StandardFonts.TimesRoman);
      const maxPageHeight = 841.89; // Maximum page height

      // Add a page to the document with A4 dimensions
      let currentPage = pdfDoc.addPage([595.28, maxPageHeight]);
      // @ts-ignore
      const { width, height } = currentPage.getSize();
      let fontSize = 20;

      currentPage.drawText("Report For: " + selectedGoal.goal_title, {
        x: 50,
        y: height - 30,
        size: fontSize,
        font: timesRomanFont,
        color: rgb(0, 0.53, 0.71),
      });

      const lines = reportText.split('\n'); // Split the text into lines based on '\n'

      let lineHeight = 16;
      let currentHeight = 60;
      fontSize = 18;
      const textColor = rgb(0, 0, 0); // Set your desired text color

      for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        let remainingText = line;
        while (remainingText.length > 0) {
          if (currentHeight >= maxPageHeight - 40) {
            // Add a new page if the current page is full
            currentPage = pdfDoc.addPage([595.28, maxPageHeight]);
            currentHeight = 30; // Reset the currentHeight for the new page
          }

          const maxChars = 60;
          let lineText = remainingText.substring(0, maxChars);
          remainingText = remainingText.substring(maxChars);
          // Check if the last character is not a whitespace, full stop (period), or newline character ('\n')
          if (!/[\s.\n]$/.test(lineText.charAt(lineText.length - 1))) {
            // Check if the character after the last character is also not a whitespace, full stop (period), or newline character ('\n')
            if (!/[\s.\n]$/.test(remainingText.charAt(0))) {
              // Add a hyphen at the end of lineText if it's not too short
              if (lineText.length > 55) {
                lineText += '-';
                remainingText = remainingText.substring(0);
              }
            }
          }

          currentPage.drawText(lineText, {
            x: 50,
            y: maxPageHeight - currentHeight,
            size: fontSize,
            font: timesRomanFont,
            color: textColor,
          });

          currentHeight += lineHeight;
        }

        currentHeight += 10; // Additional space between lines
      }

      isLoading = false;

      return pdfDoc;
    }


    async function FetchReport() {
        
        isLoading = true;
        const response = await fetch(`/api/get_report/${selected_goal.id}`); //, {method: 'GET', headers: {'Content-Type': 'application/json'}});

        if (response.status === 200) 
        {
            const reportText = await response.text();
            const pdfDoc = await generatePDF(reportText, selected_goal);
            //generate a data uri for the PDF
            const pdfBytes = await pdfDoc.save();
            pdfDataUri = URL.createObjectURL(new Blob([pdfBytes], {type: 'application/pdf'}));
            document_name = selected_goal.goal_title + " report.pdf";
            error_message = "";

            const reportDiv = document.getElementById('report');
            reportDiv.scrollIntoView({ behavior: 'smooth' });
      
            isLoading = false;
        } 
        else if (response.status === 401) 
        {
          // Redirect to the login page when Unauthorized (401) status is received
          push('/login'); 
        } 
        else 
        {
          const data = await response.json();

          error_message = data.message || "An error occurred trying to fetch report. Please contact support.";
          success_message = '';
          isLoading = false;
        }
  
        
    }
    onMount(() => {
            isLoading = true;
          });
</script>

<main>
        
    <h3>View Goal Analysis Report</h3>
    
    {#if error_message !== null}
        <p class="error-message">{error_message}</p>
    {/if}

    {#if isLoading}
        <div class="center-container">
            <Circle2 size="64" />
        </div>
    {/if}


    {#if goals.length > 0}
       <h4 class="m-3">Select a goal to view report.</h4> 
       <Listgroup>
        <ul>
            {#each goals as goal}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <li
                class="goal-item"
                on:click={() => select_goal(goal)}
                on:keydown={(event) => {
                    if (event.key === 'Enter' || event.key === 'Space') {
                        select_goal(goal);
                    }
                }}
                tabindex="-1" 
                > <!--Make the li element focusable-->
                    {goal.goal_title}
                </li>
            {/each}
        </ul>
      </Listgroup>
    {/if}

    {#if !isLoading && goals.length == 0}
      <p class="text-black"><strong>No available goals.</strong></p>
    {/if}
    
    {#if selected_goal !== null}
    <h3>Report</h3>
        <div id="report" class="report">
            {#if pdfDataUri}
                <a href={pdfDataUri} download={document_name} >Download PDF</a>
                <!-- svelte-ignore a11y-missing-attribute -->
                <iframe src={pdfDataUri} class="pdf-frame" aria-label="PDF Report"></iframe>
            {:else}
                <p>No report available</p>
            {/if}
        </div>
    {/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h3 {
		color: #ff3e00;
		text-transform: uppercase;
		font-weight: 400;
	}

  h4 {
		color:black;
		font-weight: 400;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}


    .goal-item {
        background-color: #008080;
        border: 1px solid #ddd;
        color:black;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }

    .goal-item:focus,
    .goal-item:hover {
        background-color: #e0e0e0;
        outline: none;
    }

    .error-message {
        color: red;
        font-size: 14px;
        margin-top: 4px;
    }

    .report {
        margin-top: 20px;
        border: 1px solid #ccc;
        padding: 10px;
        background-color: #f9f9f9;
        overflow: auto; /* Enable scrolling if the content overflows */
        white-space: pre-wrap; /* Preserve line breaks and wrap long lines */
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.5;
    }

    .pdf-frame {
        width: 100%;
        height: 50vh; /* Adjust the height as needed */
        border: none;
    }

    @media (max-width: 640px) {
        .pdf-frame {
            height: 400px; /* Adjust the height for smaller screens */
            width: fit-content;
        }
    }

     .center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
        
      }
</style>