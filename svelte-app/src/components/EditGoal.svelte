<script>
    import {push} from 'svelte-spa-router';

    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';

    let isLoading = false;
    let goals = [];

    let timezones = [];

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

    async function fetch_timezones(){
        isLoading = true;
        const response = await fetch(`/api/get_timezones`, myInit);

        if(response.ok){
            timezones = await response.json();
            isLoading = false;
        }else{
            error_message = "An error occurred fetching timezones";
            success_message = '';
            isLoading = false;
        }
        
    }

    fetch_timezones()

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

    async function select_goal(goal){
        selected_goal = goal;
    }

    async function EditGoal() {
        isLoading = true;
        const goal_data = selected_goal
        alert(JSON.stringify(goal_data))
        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch('/api/edit_goal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            }, 
            body: JSON.stringify({goal_data})
        });

        if(!response.ok){
            error_message = "Error editing goal";
            success_message = '';
            isLoading = false;
        }else{
            error_message = '';
            success_message = 'Goal edited successfully';
            isLoading = false;
        }

   }

    function handleInput(event) {
    let inputValue = parseInt(event.target.value);

    // Clamp the input value within the range of 1 to 365
    selected_goal.report_frequency = Math.min(Math.max(inputValue, 1), 365);
  }


  onMount(() => {
          // Reset isLoading state when the component is mounted
          isLoading = false;
        });
</script>

<main >
    <button on:click={() => push('/dashboard')}>Dashboard</button> 
    
    <h1>Edit Goals</h1>
    {#if isLoading}
        <div class="center-container">
            <Circle2 size="64" />
        </div>
    {/if}
    <button  on:click= {fetchGoals}>Fetch Goals</button>

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
    <form on:submit|preventDefault={EditGoal}> 
        <h1>Edit goal</h1>
        {#if error_message != ''}
            <p class="error-message">{error_message}</p>
        {:else if success_message != ''}
            <p class="success-message">{success_message}</p>
        {/if}
        <hr/>
        <label>
            Goal Title: <input type="text" bind:value={selected_goal.goal_title} required />
        </label>
        <label>
            Goal Description: <textarea bind:value={selected_goal.goal_description} required />
        </label>
        <label>
            Time of Day: <input type="time" bind:value={selected_goal.time_of_day} required />
        </label>
        <label>
            Timezone:
            <select bind:value={selected_goal.time_zone}>
                {#each timezones as timezone}
                    <option value={timezone}>{timezone}</option>
                {/each}
            </select>
        </label>
        <label>
            Contact Choice:
            <select bind:value={selected_goal.contact_choice}>
                <option value="SMS">SMS</option>
                <option value="WhatsApp">WhatsApp</option>
            </select>
        </label>

        <label>
            Report Frequency: <input type="number" bind:value={selected_goal.report_frequency} on:input={handleInput} min={1} max={365} required />
        </label>

        <button type="submit">Update Goal</button>
    </form>
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