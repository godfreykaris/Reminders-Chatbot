<script>
    import { push } from "svelte-spa-router";

    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';

    let isLoading = false;

    let goals = [];
    let error_message = '';
    
    let headers = new Headers();

    headers.append('Accept', 'application/json');
    let csrf = document.getElementsByName("csrf-token")[0].content;
    headers.append("X-CSRFToken", csrf);

    const myInit = {
      method: "GET",
      credentials: "same-origin",
      headers: headers,
    };

    async function fetchGoals() {
        isLoading = true;
        const response = await fetch(`/api/get_goals`, myInit);
        
        if(response.ok){
            goals = await response.json();
            isLoading = false;
        }else{
            error_message = "An error occurred fetching goals";
            success_message = '';
            isLoading = false;
        }
    }

    fetchGoals();
</script>


<main>
    <button on:click={() => push('/dashboard')}>Dashboard</button>
    {#if isLoading}
        <div class="center-container">
            <Circle2 size="64" />
        </div>
    {/if}
    
    <div class="center-container">
           <table>
                <thead>
                    <tr>
                        <th>Goal Title</th>
                        <th>Goal Description</th>
                        <th>Time of Day</th>
                        <th>Time Zone</th>
                        <th>Contact Choice</th>
                        <th>Report Frequency</th>
                    </tr>
                </thead>
                <tbody>
                    {#each goals as goal}
                        <tr>
                            <td>{goal.goal_title}</td>
                            <td>{goal.goal_description}</td>
                            <td>{goal.time_of_day}</td>
                            <td>{goal.time_zone}</td>
                            <td>{goal.contact_choice}</td>
                            <td>{goal.report_frequency}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
    </div>

    
</main>

<style>
    main {
		text-align: center;
		padding: 1em;
		max-width: 80vw;
		margin: 0 auto;
	}

    table {
      width: 100%;
      border-collapse: collapse;
      border: 1px solid #ccc;
    }
  
    th, td {
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #ccc;
    }
  
    th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
  
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }

    .center-container {
    display: flex;
    flex-direction: column; /* Center vertically */
    justify-content: center; /* Center vertically */
    align-items: center; /* Center horizontally */
  }
  </style>