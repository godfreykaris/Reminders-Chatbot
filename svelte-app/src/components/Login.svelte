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


      if (response.status === 200) {
        // Authentication successful
        message = data.message;
        isLoading = false;
        push('/dashboard') // Redirect to the dashboard
      } else if (response.status === 401) 
      {
        // Authentication failed
        message = 'Authentication failed. Please check your credentials.';
        isLoading = false;
      } 
      else {
        message = "An error occurred while trying to log in. Make sure your details are correct.";
        isLoading = false;
      }
      
    }
    catch (error) 
     {
      console.error('Error:', error);
      message = 'An error occurred while trying to log in. Please try again.';
      alert(message)
      location.reload();
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


</style>

{#if is_forgot_password_modal_open}
  <ForgotPassword  on:closeModal={() => {is_forgot_password_modal_open = false; }} />
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

