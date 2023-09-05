<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
  
    export let selectedGoal;

    let isLoading = false;
    let error_message = '';
    let success_message = '';
    let timezones = [];

    const dispatch = createEventDispatcher();

    function closeModal() {
      dispatch('closeModal');
    }
  
    async function fetchTimezones() {
        isLoading = true;
  
        let headers = new Headers();
        headers.append('Accept', 'application/json');
        let csrf = document.getElementsByName("csrf-token")[0].content;
        headers.append("X-CSRFToken", csrf);

        const myInit = {
          method: "GET",
          credentials: "same-origin",
          headers: headers,
        };

        const response = await fetch(`/api/get_timezones`, myInit);
    
       
        if (response.status === 200)
        {
          timezones = await response.json();
          isLoading = false;
        }
        else if (response.status === 401)
        {
          // Redirect to the login page when Unauthorized (401) status is received
          push('/login'); 
        } 
        else 
        {
          error_message = "An error occurred trying to fetch timezones";
          success_message = '';
          isLoading = false;
          location.reload();
        }
     }
  
    fetchTimezones();
  
    // Function to handle goal editing
    async function editGoal() {
        isLoading = true;
        const goal_data = selectedGoal
        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch('/api/edit_goal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            }, 
            body: JSON.stringify({goal_data})
        });

        
        if (response.status === 200)
        {
            error_message = '';
            success_message = 'Goal edited successfully';
            isLoading = false;        

            closeModal();
            location.reload();
        }
        else if (response.status === 401)
        {
          // Redirect to the login page when Unauthorized (401) status is received
          push('/login'); 
        } 
        else 
        {
          error_message = "Error editing goal";
          success_message = '';
          isLoading = false;
          location.reload();
        }

    }
  
    function handleInput(event) {
      let inputValue = parseInt(event.target.value);
      // Clamp the input value within the range of 1 to 365
      selectedGoal.report_frequency = Math.min(Math.max(inputValue, 1), 365);
    }
  
    onMount(() => {
      // Reset isLoading state when the component is mounted
      isLoading = false;
    });
  </script>
  
  <div class="modal-overlay">
    <div class="modal">
      <h1>Edit Goal</h1>
      {#if isLoading}
        <div class="center-container">
          <Circle2 size="64" />
        </div>
      {:else}
        <form on:submit|preventDefault={editGoal}>
          {#if error_message != ''}
            <p class="error-message">{error_message}</p>
          {:else if success_message != ''}
            <p class="success-message">{success_message}</p>
          {/if}
          <hr />
          <label>
            Goal Title: <input type="text" bind:value={selectedGoal.goal_title} required />
          </label>
          <label>
            Goal Description: <textarea bind:value={selectedGoal.goal_description} required />
          </label>
          <label>
            Time of Day: <input type="time" bind:value={selectedGoal.time_of_day} required />
          </label>
          <label>
            Timezone:
            <select required bind:value={selectedGoal.time_zone}>
              {#each timezones as timezone}
                <option value={timezone}>{timezone}</option>
              {/each}
            </select>
          </label>
          <label>
            Contact Choice:
            <select required bind:value={selectedGoal.contact_choice}>
              <option value="SMS">SMS</option>
              <option value="WhatsApp">WhatsApp</option>
            </select>
          </label>
          <label>
            Report Frequency(Get a report  after the specified days): <input type="number" bind:value={selectedGoal.report_frequency} on:input={handleInput} min={1} max={365} required />
          </label>
          <button type="submit">Update Goal</button>
          <button on:click={closeModal}>Cancel</button>
        </form>
      {/if}
    </div>
  </div>
  
  <style>
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }
  
    .modal {
      background-color: white;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      text-align: center;
      max-width: 300px;
    }
      
    h1 {
      color: #ff3e00;
      text-transform: uppercase;
      font-size: 4em;
      font-weight: 100;
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
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
  </style>
  