<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
  
    export let selectedGoal;

    let isLoading = false;
    let error_message = '';
    let success_message = '';
    

    const dispatch = createEventDispatcher();

    function closeModal() {
      dispatch('closeModal');
    } 
    
  
    async function deleteGoal() {
        if(!selectedGoal)
            return;
            
        const confirm_delete = window.confirm("Are you sure you want to delete this goal?");

        if(!confirm_delete)
            return

        isLoading = true;   

        let csrf = document.getElementsByName("csrf-token")[0].content;
        const response = await fetch(`/api/delete_goal`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            }, 
            body: JSON.stringify({id: selectedGoal.id})
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
            alert(success_message);
            closeModal();
            location.reload();
        }
        
          
    }
      
    onMount(() => {
      // Reset isLoading state when the component is mounted
      isLoading = false;
    });
  </script>
  
  <div class="modal-overlay">
    <div class="modal">
      <h1>Delete Goal</h1>
      {#if isLoading}
        <div class="center-container">
          <Circle2 size="64" />
        </div>
      {:else}
        <form on:submit|preventDefault={deleteGoal}>
          {#if error_message != ''}
            <p class="error-message">{error_message}</p>
          {:else if success_message != ''}
            <p class="success-message">{success_message}</p>
          {/if}
          <hr />
          
          <h2> Goal Title: {selectedGoal.goal_title}  </h2>
          
          <button type="submit">Delete Goal</button>
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
  