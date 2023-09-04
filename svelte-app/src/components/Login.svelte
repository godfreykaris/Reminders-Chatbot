<script>
  import {push} from 'svelte-spa-router';

  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';

  import ForgotPassword from './ForgotPassword.svelte';


  let isLoading = false;

  let username = '';
  let password = '';
  let message = ''; // Initialize response message variable

  let is_forgot_password_modal_open = false;

  function handle_forgot_password_click(){
    is_forgot_password_modal_open = true;
  }

  function handle_close_modal(){
    is_forgot_password_modal_open = false;
  }


  // Function to handle login
  async function handleLogin() {
    isLoading = true;
    try {
      let csrf = document.getElementsByName("csrf-token")[0].content;
      const response = await fetch('/api/login', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
        }, 
        body: JSON.stringify({ username, password }), // Send the username and password
      });

      const data = await response.json();

      if (response.ok) {
        // Authentication successful
        message = data.message;
        isLoading = false;
       push('/dashboard') // Redirect to the dashboard
      } else {
        // Authentication failed
        message = data.message; //'Authentication failed. Please check your credentials.';
        isLoading = false;
      }
    } catch (error) {
      console.error('Error:', error);
      message = 'An error occurred while trying to log in. Please try again later.';
      isLoading = false;
    }
  }
  onMount(() => {
            // Reset isLoading state when the component is mounted
            isLoading = false;
          });
</script>

<style>
  .center-container {
    display: flex;
    flex-direction: column; /* Center vertically */
    justify-content: center; /* Center vertically */
    align-items: center; /* Center horizontally */
    height: 100vh; /* 100% viewport height to fill the entire screen */
  }

  input{
    border: solid black 1px;
  } 

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

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
    z-index: 1;
    overflow: auto;
  }

  /* Modal content styles */
  .modal-content {
    position: relative;
    margin: 15% auto; /* Center the modal vertically */
    width: 60%;
    max-width: 400px; /* Limit the modal width */
    background-color: #fff;
    padding: 20px;
    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.2); /* Box shadow for a subtle elevation effect */
    border-radius: 8px;
  }

  /* Close button styles */
  .modal-content button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: transparent;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
</style>

{#if is_forgot_password_modal_open}
    <div class="modal">
      <div class="modal-content">
        <button on:click={handle_close_modal}>&times;</button>
        <ForgotPassword/>
      </div>
    </div>
{/if}


<main>
  <div class="center-container">
    <button on:click={() => push('/')}>Home</button>
    <h1>LOGIN</h1>
    <!-- Display the message if it's not empty -->
    {#if message}
      <p class='error-message'>{message}</p>
    {/if}
    {#if isLoading}
      <Circle2 size="64" />
    {/if}    

    <form on:submit|preventDefault={handleLogin}>
      <label for="username">Email/Phone</label>
      <input type="text" id="username" bind:value={username} />

      <label for="password">Password</label>
      <input type="password" id="password" bind:value={password} />
      <br>
      <button type="submit">Login</button>

      <br/>
      <!-- svelte-ignore a11y-invalid-attribute -->
      <button on:click={handle_forgot_password_click}>Forgot Password</button>
    </form>    
  </div>  
</main>

