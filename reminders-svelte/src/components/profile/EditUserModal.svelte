<!-- EditUserModal.svelte -->
<script lang='ts'>
  import { Circle2 } from 'svelte-loading-spinners';
  import {push} from 'svelte-spa-router';
  import { createEventDispatcher } from 'svelte';

  import { Button, Label, Input } from 'flowbite-svelte';


  export let editedUser;
  let newUser = editedUser;

  
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
    if (!newUser.name || !newUser.email || !newUser.phone) {
      errorMessage = 'Please fill in all fields.';
      return;
    }

    isLoading = true;

    // @ts-ignore
    let csrf = document.getElementsByName('csrf-token')[0].content;

    // Send the edited user data to your API endpoint
    const response = await fetch('/api/edit_user', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
      },
      body: JSON.stringify({ user: newUser }),
    });

    isLoading = false;
    if (response.status === 200)
    {
      closeModal();
    } 
    else if (response.status === 401)
    {
      // Redirect to the login page when Unauthorized (401) status is received
      push('/login'); 
    } 
    else {
      errorMessage = "An error occurred trying to editing user";
      successMessage = '';
      isLoading = false;
    }  
  }
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
  <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Update Profile</h3>
  <!-- Show loading indicator while isLoading is true -->
  {#if isLoading}
    <div class="flex items-center justify-center">
      <Circle2 size="64" />
    </div>
  {/if}
  
  <!-- Display error or success message based on conditions -->
  {#if errorMessage}
    <p class="error-message">{errorMessage}</p>
  {:else if successMessage}
    <p class="success-message">{successMessage}</p>
  {/if}

  <Label class="space-y-2">
    <span>Name</span>
    <Input type="text" name="name" bind:value={newUser.name} placeholder="John Doe" class="border-1 border-black" required />
  </Label>
  <Label class="space-y-2">
    <span>Email</span>
    <Input type="email" name="email" bind:value={newUser.email} placeholder="name@company.com" class="border-1 border-black" required />
  </Label>
  <Label class="space-y-2">
    <span>Phone</span>
    <Input type="text" name="phone" bind:value={newUser.phone} placeholder="+1123456789" class="border-1 border-black" required />
  </Label>
  <Button on:click={editUser} class="w-full1">Update Profile</Button>
</form>


