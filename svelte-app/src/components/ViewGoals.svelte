<script>
    import { push } from "svelte-spa-router";

    let goals = [];
    let error_message = '';

    let user_id = 6;

    async function FetchGoals() {
        try {
            const response = await fetch(`/api/view_goals`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "user_id": user_id })
            });

            if (response.ok) {
                goals = await response.json(); // Await the response.json()
                error_message = '';
                console.log("Success!")
            } else {
                error_message = 'Invalid data format returned;'
                console.log("Failed");
            }
        } catch (error) {
            error_message = error;
            console.log("Error", error);
        }
    }

    FetchGoals();
</script>


<div class="center-container">
    <button on:click={() => push('/dashboard')}>Dashboard</button>

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

<style>
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
    height: 100vh; /* 100% viewport height to fill the entire screen */
  }
  </style>