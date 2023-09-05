<!-- EditUserModal.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';

  export let editedUser;

  let isLoading = false;
  let errorMessage = '';
  let successMessage = '';

  const dispatch = createEventDispatcher();

  function closeModal() {
    dispatch('closeModal');
  }

  async function editUser() {
    // Reset error and success messages
    errorMessage = '';
    successMessage = '';

    // Validate and edit the user's details
    if (!editedUser.name || !editedUser.email || !editedUser.phone) {
      errorMessage = 'Please fill in all fields.';
      return;
    }

    isLoading = true;

    let csrf = document.getElementsByName('csrf-token')[0].content;

    // Send the edited user data to your API endpoint
    const response = await fetch('/api/edit_user', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
      },
      body: JSON.stringify({ user: editedUser }),
    });

    isLoading = false;

    if (response.status === 401)
    {
      // Redirect to the login page when Unauthorized (401) status is received
      push('/login'); 
    } 
    else {
      errorMessage = "An error occurred trying to editing user";
      successMessage = '';
      isLoading = false;
      location.reload();
    }

    closeModal();
  
  }
</script>

<div class="modal-overlay">
  <div class="modal">
    <h1>Edit User</h1>
    {#if isLoading}
      <div class="center-container">
        <Circle2 size="64" />
      </div>
    {:else}
      {#if errorMessage}
        <p class="error-message">{errorMessage}</p>
      {:else if successMessage}
        <p class="success-message">{successMessage}</p>
      {/if}
      <form on:submit|preventDefault={editUser}>
        <label>
          Name: <input type="text" bind:value={editedUser.name} required />
        </label>
        <label>
          Email: <input type="text" bind:value={editedUser.email} required />
        </label>
        <label>
          Phone: <input type="text" bind:value={editedUser.phone} maxlength="13" required />
        </label>
        <button type="submit">Update User</button>
        <button on:click={closeModal}>Cancel</button>
      </form>
    {/if}
  </div>
</div>

<style>
  /* Styles for the modal dialog */
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
    z-index: 1000; /* Ensure it's on top of everything */
  }

  .modal {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .center-container {
    display: flex;
    flex-direction: column; /* Center vertically */
    justify-content: center; /* Center vertically */
    align-items: center; /* Center horizontally */
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

  /* Add more styling as needed */
</style>
