<script>
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import {push} from 'svelte-spa-router';
    import { Button, Label, Input, Textarea } from 'flowbite-svelte';
    import { createEventDispatcher } from 'svelte';

    export let selectedGoal;

    let isLoading = false;
    let error_message = '';
    let success_message = '';
    let timezones = [];

    const dispatch = createEventDispatcher();

    async function fetchTimezones() {
        isLoading = true;
  
        let headers = new Headers();
        headers.append('Accept', 'application/json');
        // @ts-ignore
        let csrf = document.getElementsByName("csrf-token")[0].content;
        headers.append("X-CSRFToken", csrf);

        const myInit = {
          method: "GET",
          credentials: 'same-origin',
          headers: headers,
        };

        // @ts-ignore
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
        }
     }
  
    fetchTimezones();
  
    // Function to handle goal editing
    async function editGoal() {
        isLoading = true;

        const goal_data = selectedGoal
        // @ts-ignore
        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch('/api/edit_goal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            }, 
            body: JSON.stringify({goal_data})
        });

        
        if (response.ok) {
          error_message = '';
          success_message = 'Goal edited successfully';
          isLoading = false;
          alert(success_message)

          // Emit the edited goal to the parent component
          dispatch('goalEdited', { editedGoal: selectedGoal });
        } else if (response.status === 401) {
          push('/login');
        } else {
          error_message = "Error editing goal";
          success_message = '';
          isLoading = false;
          alert(error_message)
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
  
  <style>
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

  <form class="flex flex-col space-y-6" action="#">
    <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reminders  </h3>
    <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Edit Goal</h3>
    <Label class="space-y-2">
      <span>Goal Title</span>
      <Input type="text" name="goal_title" bind:value={selectedGoal.goal_title} class="border-1 border-black" required />
    </Label>

    <Label class="space-y-2">
      <span>Goal Description</span>
      <Textarea name="goal_description" bind:value={selectedGoal.goal_description} class="border-1 border-black" required />
    </Label>

    <Label class="space-y-2">
      <span>Time of Day e.g. 00:00 AM</span>
      <Input type="time" name="time_of_day" bind:value={selectedGoal.time_of_day} class="border-1 border-black" required />
    </Label>

    <Label class="space-y-2">
      <span>Timezone</span>
      <select name="time_zone" bind:value={selectedGoal.time_zone} class="items-center border-1 border-black" required>
        {#each timezones as timezone}
          <option value={timezone}>{timezone}</option>
        {/each}
      </select>
    </Label>

    <Label class="space-y-2">
      <span>Contact Choice</span>
      <select name="contact_choice" bind:value={selectedGoal.contact_choice} class="items-center" required>
        <option value="SMS">SMS</option>
        <option value="WhatsApp">WhatsApp</option>
      </select>
    </Label>

    <Label class="space-y-2">
      <span>Report Frequency (Get a report after the specified days)</span>
      <Input type="number" name="report_frequency" bind:value={selectedGoal.report_frequency} on:input={handleInput} min={1} max={365} required />
    </Label>
    <!-- Show loading indicator while isLoading is true -->
    {#if isLoading}
      <div class="flex items-center justify-center">
        <Circle2 size="64" />
      </div>
    {/if}
    
    <!-- Display error or success message based on conditions -->
    {#if error_message}
      <p class="error-message">{error_message}</p>
    {:else if success_message}
      <p class="success-message">{success_message}</p>
    {/if}
    <hr/>
    <Button on:click={editGoal}>Update Goal</Button>
  </form>