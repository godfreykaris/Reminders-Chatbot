<!-- AddGoalModal.svelte -->
<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
  
    let isLoading = false;
    let report_frequency = 1;
    let goal_title = '';
    let goal_description = '';
    let time_of_day = '';
    let time_zone = '';
    let contact_choice = '';
    const choices = ["WhatsApp", "SMS"];
  
    let error_message = '';
    let success_message = '';

    const dispatch = createEventDispatcher();

    function closeModal() {
      dispatch('closeModal');
    }
  
    let timezones = [];

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
  
      if (response.ok) {
        timezones = await response.json();
        isLoading = false;
      } else {
        error_message = "An error occurred trying to fetch timezones";
        success_message = '';
        isLoading = false;
      }
    }
  
    fetchTimezones();
  
    async function addGoal() {
      isLoading = true;
      const goal_data = {
        report_frequency,
        goal_title,
        goal_description,
        time_of_day,
        time_zone,
        contact_choice
      };
  
      let csrf = document.getElementsByName("csrf-token")[0].content;
      const response = await fetch('/api/add_goal', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify({ goal_data })
      });
  
      if (!response.ok) {
        error_message = "An error occurred trying to add a goal";
        success_message = '';
        isLoading = false;
      } else {
        error_message = '';
        success_message = 'Goal added successfully';
        isLoading = false;

        alert(success_message);
        closeModal();
        location.reload();
      }
    }
  
    function handleInput(event) {
      let inputValue = parseInt(event.target.value);
  
      // Clamp the input value within the range of 1 to 365
      report_frequency = Math.min(Math.max(inputValue, 1), 365);
    }
  
    onMount(() => {
      // Reset isLoading state when the component is mounted
      isLoading = false;
    });
  </script>

  
  <div class="modal-overlay">
    <div class="modal">
        <h1>Add a Goal</h1>
        {#if error_message != ''}
          <p class="error-message">{error_message}</p>
        {:else if success_message != ''}
          <p class="success-message">{success_message}</p>
        {/if}
               {#if isLoading}
          <div class="center-container">
            <Circle2 size="64" />
          </div>
        {/if}
               <hr />
               <form on:submit|preventDefault={addGoal}>
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
              <option style="text-align: center;" value="">---Select---</option>
              {#each timezones as timezone}
                <option value={timezone}>{timezone}</option>
              {/each}
            </select>
          </label>
          <label>
            Contact Choice:
            <select bind:value={contact_choice}>
              <option value="">---Select---</option>
              {#each choices as choice}
                <option value={choice}>{choice}</option>
              {/each}
            </select>
          </label>
          <label>
            Report Frequency: <input type="number" bind:value={report_frequency} on:input={handleInput} min={1} max={365} required />
          </label>
          <button type="submit">Create Goal</button>
          <button on:click={closeModal}>Cancel</button>
        </form>
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
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      text-align: center;
      max-width: 400px;
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
  