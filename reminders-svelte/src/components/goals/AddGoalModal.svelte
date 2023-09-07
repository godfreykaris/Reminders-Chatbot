<!-- AddGoalModal.svelte -->
<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import { Button, Label, Input, Textarea } from 'flowbite-svelte';
    import {push} from 'svelte-spa-router';

  
    let isLoading = false;
    let report_frequency = 1;
    let goal_title = '';
    let goal_description = '';
    let time_of_day = '';
    let time_zone = '';
    let contact_choice = '';
   
  
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
      // @ts-ignore
      let csrf = document.getElementsByName("csrf-token")[0].content;
      headers.append("X-CSRFToken", csrf);
  
      const myInit = {
        method: "GET",
        credentials: "same-origin",
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
          location.reload()
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
  
      // @ts-ignore
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
  
      if (response.status === 200)
        {
          error_message = '';
          success_message = 'Goal added successfully';
          isLoading = false;
          alert(success_message);

          closeModal();
          
        }
        else if (response.status === 401)
        {
          // Redirect to the login page when Unauthorized (401) status is received
          push('/login'); 
        } 
        else 
        {
          error_message = "An error occurred trying to add a goal";
          success_message = '';
          isLoading = false;
          
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
  <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Add Goal</h3>
   
  <Label class="space-y-2">
    <span>Goal Title</span>
    <Input type="text" name="goal_title" bind:value={goal_title} class="border-1 border-black" required />
  </Label>

  <Label class="space-y-2">
    <span>Goal Description</span>
    <Textarea name="goal_description" bind:value={goal_description} class="border-1 border-black" required />
  </Label>

  <Label class="space-y-2">
    <span>Time of Day e.g. 00:00 AM</span>
    <Input type="time" name="time_of_day" bind:value={time_of_day} class="justify-center border-1 border-black" required />
  </Label>

  <Label class="space-y-2">
    <span>Timezone</span>
    <select name="time_zone" bind:value={time_zone} class="items-center justify-center border-1 border-black" required>
      <option value="">--- Select ---</option>
      {#each timezones as timezone}
        <option value={timezone}>{timezone}</option>
      {/each}
    </select>
  </Label>

  <Label class="space-y-2">
    <span>Contact Choice</span>
    <select name="contact_choice" bind:value={contact_choice} class="items-center border-1 border-black" required>
      <option value="">--- Select ---</option>
      <option value="SMS">SMS</option>
      <option value="WhatsApp">WhatsApp</option>
    </select>
  </Label>

  <Label class="space-y-2">
    <span>Report Frequency (Get a report after the specified days)</span>
    <Input type="number" name="report_frequency" bind:value={report_frequency} on:input={handleInput} min={1} max={365} required />
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
   
  <Button on:click={addGoal}>Add Goal</Button>

  </form>