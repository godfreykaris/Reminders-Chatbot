<script>
    import {push} from 'svelte-spa-router';
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';

    let isLoading = false;

    let goals = [];

    let selected_goal = null;

    let error_message = '';
    let success_message = '';

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

        if(response.ok)
        {
            goals = await response.json();
            error_message = '';
            success_message = 'Goals fetched successfully';
            isLoading = false;
        }           
        else
        {
            error_message = "An error occurred trying to fetch goals";
            success_message = '';
            isLoading = false;
        }
    }

    async function select_goal(goal){
        selected_goal = goal;
    }

    async function DeleteGoal() {
        if(!select_goal)
            return;

        isLoading = true;   

        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch(`/api/delete_goal`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            }, 
            body: JSON.stringify({id: selected_goal.id})
        });

        if(!response.ok)
        {
            error_message = "An error occurred";
            success_message = '';
            isLoading = false;
        }
        else
        {
            error_message = "";
            success_message = 'Goal deleted successfully.';
            isLoading = false;
        }
        
        selected_goal = null;
        fetchGoals(); // Refresh the goals list after deletion
    }

</script>

<main class="center-container">
    <button on:click={() => push('/dashboard')}>Dashboard</button>
    <h1>Delete Goal</h1>

    {#if error_message != ''}
        <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
        <p class="success-message">{success_message}</p>
    {/if}
    {#if isLoading}
         <Circle2 size="64" />
    {/if}
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
        <button on:click={DeleteGoal}>Delete Goal</button>
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

    button{
        background-color: #ff150088;
    }

    .error-message {
        color: red;
        font-size: 14px;
        margin-top: 4px;
    }

    .success-message {
        color: green;
        font-size: 14px;
        margin-top: 4px;
    }

    .center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
        
      }
</style>