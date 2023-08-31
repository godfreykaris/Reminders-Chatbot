<script>
    import {push} from 'svelte-spa-router';
    import {PDFDocument} from 'pdf-lib';

    let goals = [];

    let selected_goal = null;

    let error_message = '';

    let pdfDataUri = null;


    async function fetchGoals() {
        const response = await fetch('/api/get_goals');
        
        if(response.ok){
            goals = await response.json();
        }else{
            error_message = "An error occurred fetching goals";
        }
    }

    async function select_goal(goal){
        selected_goal = goal;
        await FetchReport();
    }

    async function FetchReport() {
        const response = await fetch(`/api/get_report/${selected_goal.id}/${selected_goal.user_id}`); //, {method: 'GET', headers: {'Content-Type': 'application/json'}});

        if(response.ok){
            const reportText = await response.text();

            //create a new pdf document
            const pdfDoc = await PDFDocument.create();

            //add a page to the document
            const page = pdfDoc.addPage([600, 400]);

            //embed the text content into the 
            page.drawText(reportText, {
                x: 50,
                y: 350,
                size: 12, 
            });

            //generate a data uri for the PDF
            const pdfBytes = await pdfDoc.save();
            pdfDataUri = URL.createObjectURL(new Blob([pdfBytes], {type: 'application/pdf'}));

            error_message = "";
        }else{
            error_message = 'Error fetching report';
        }

        // const data = await response.json();
        // console.log(data.message);
    }
</script>

<main>
    <button on:click={() => push('/dashboard')}>Dashboard</button>
    
    {#if error_message !== null}
        <p class="error-message">{error_message}</p>
    {/if}

    <h1>View Goal Analysis Report</h1>
    <button on:click= {fetchGoals}>Fetch Goals</button>

    {#if goals.length > 0}
        <ul class="goal-list">
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
    {:else}
        <p>No goals fetched</p>
    {/if}
    
    {#if selected_goal !== null}
    <h1>Report</h1>
        <div class="report">
            {#if pdfDataUri}
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

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

    .goal-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .goal-item {
        background-color: #f4f4f4;
        border: 1px solid #ddd;
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
        height: 100%; /* Adjust the height as needed */
        border: none;
    }

    @media (max-width: 640px) {
        .pdf-frame {
            height: 400px; /* Adjust the height for smaller screens */
            width: fit-content;
        }
    }
</style>