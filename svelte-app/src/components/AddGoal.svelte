<script>

    let report_frequency = 1;
    let goal_title = '';
    let goal_description = '';
    let time_of_day = '';
    let time_zone = '';
    let contact_choice = '';

    let timezones = [];

    const choices = ["WhatsApp", "SMS"];

    let error_message = '';
    let success_message = '';

    
    async function fetch_timezones(){
        let headers = new Headers();

        headers.append('Accept', 'application/json');

        const myInit = {
          method: "GET",
          mode: 'cors',
          credentials: 'include',
          headers: headers,
        };

        const response = await fetch(`/api/get_timezones`, myInit);
        
        if(response.ok){
            timezones = await response.json();
        }else{
            error_message = "An error occurred trying to fetch timezones";
            success_message = '';
        }
    }

    fetch_timezones();

    async function AddGoal() {
        const formData = {
            report_frequency,
            goal_title,
            goal_description,
            time_of_day,
            time_zone,
            contact_choice
        };
    
        const response = await fetch('/api/add_goal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if(!response.ok){
            error_message = "An error occurred trying to add a goal";
            success_message = ''
        }
        else
        {
            error_message = '';
            success_message = 'Goal added successfully';
        }
    
    }

    function handleInput(event) {
    let inputValue = parseInt(event.target.value);

    // Clamp the input value within the range of 1 to 365
    report_frequency = Math.min(Math.max(inputValue, 1), 365);
  }
</script>

<main>
    <button on:click={() => push('/dashboard')}>Dashboard</button>
    <h1>Add a Goal</h1>
    {#if error_message != ''}
        <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
        <p class="success-message">{success_message}</p>
    {/if}
    <hr/>
    <form on:submit|preventDefault={AddGoal}> 
        <label>
            Goal Title: <input type="text" bind:value={goal_title} required />
        </label>
        <label>
            Goal Description: <textarea bind:value={goal_description} required />
        </label>
        <label>
            Time:
            <input type="time" bind:value={time_of_day} required />
        </label>
        <label>
            Timezone:
            <select bind:value={time_zone}>
                {#each timezones as timezone}
                    <option value={timezone}>{timezone}</option>
                {/each}
            </select>
        </label>
        <label>
            Contact Choice:
            <select bind:value={contact_choice}>
                {#each choices as choice}
                    <option value={choice}>{choice}</option>                    
                {/each}
            </select>
        </label>
        
        <label>
            Report Frequency: <input type="number" bind:value={report_frequency} on:input={handleInput} min={1} max={365} required />
        </label>

        <button type="submit">Create Goal</button>
    </form>
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
</style>
