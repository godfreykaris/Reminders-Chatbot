<script>
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import {push} from 'svelte-spa-router';
    import { Button } from 'flowbite-svelte';

  
    export let selectedGoal;
    export let updateGoals;

    let isLoading = false;
    let error_message = '';
    let success_message = '';
       
  
    async function deleteGoal() {
      if (!selectedGoal) return;
        
      const confirm_delete = window.confirm("Are you sure you want to delete this goal?");
        
      if (!confirm_delete) return;
        
      isLoading = true;
        
      // @ts-ignore
      let csrf = document.getElementsByName("csrf-token")[0].content;
        
      const response = await fetch(`/api/delete_goal`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify({ id: selectedGoal.id })
      });
    
      if (response.status === 200) {
        error_message = "";
        success_message = 'Goal deleted successfully.';
        isLoading = false;
        alert(success_message);
      
        // Update the component state or trigger a callback function to handle the successful deletion
        updateGoals(selectedGoal);
      } else if (response.status === 401) {
        // Redirect to the login page when Unauthorized (401) status is received
        push('/login');
      } else {
        error_message = "An error occurred while trying to delete the goal";
        success_message = '';
        isLoading = false;
      }
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
    <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Delete Goal</h3>
    <!-- Show loading indicator while isLoading is true -->
      {#if isLoading}
      <div class="flex items-center justify-center">
        <Circle2 size="64" />
      </div>
    {/if}
    
    {#if error_message != ''}
      <p class="error-message">{error_message}</p>
    {:else if success_message != ''}
      <p class="success-message">{success_message}</p>
    {/if}
    <hr />
    
    <h2> Goal Title: {selectedGoal.goal_title}  </h2> 
    
  
    <Button on:click={deleteGoal}>Delete Goal</Button>
  
    </form>