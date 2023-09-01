<script>
  import { push } from "svelte-spa-router";
  
  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';

  let isLoading = false;

  let name =   '' ;
  let email = '';
  let phone = '';
  let password = '';
  let confirmPassword = '';
  let error_message = ''; // Initialize response message variable
  let success_message = ''; // Initialize response message variable


  async function handleRegister() {
    success_message = "";
    error_message = "";
    isLoading = true;
    try {
      let csrf = document.getElementsByName("csrf-token")[0].content;
      const response = await fetch(`/api/register`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
        }, 
        body: JSON.stringify({
          phone: phone,
          name: name,          
          email: email,
          password: password,
        }),
      });

      const data = await response.json();
      
      if (response.ok) 
      {

        // Registration successful
        console.log('User registered successfully');
        success_message = data.message; // Set the error message from the response
        error_message = "";
        isLoading = false;

      } 
      else 
      {
        // Registration failed, handle errors
        error_message = data.message; // Set the error message from the response
        success_message = "";
        console.error('Registration failed:', error_message);
        isLoading = false;
      }
    } catch (error) {
      // Network or other error occurred
      error_message = 'An error occurred while registering.';
      success_message = "";
      console.error('Error:', error);
      isLoading = false;
    }
  }
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
    border: solid black 2px;
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

  .success-message {
      color: green;
      font-size: 14px;
      margin-top: 4px;
  }
  
</style>

<main class="center-container">
  <h1> REGISTER </h1>
  <button on:click={() => push('/')}>Home</button>
  <!-- Display the message if it's not empty -->
  {#if error_message}
    <p class="error-message">{error_message}</p>
  {:else}
        <p class="success-message">{success_message}</p>
  {/if}

  {#if isLoading}
        <div style="margin-bottom: 10px">
            <Circle2 size="64" />
        </div>
    {/if}
  
  <form>
    <label for="name">Name</label>
    <input type="name" id="name" bind:value={name} />

    <label for="email">Email</label>
    <input type="email" id="email" bind:value={email} />

    <label for="phone">Phone</label>
    <input type="phone" id="phone" bind:value={phone} />
  
    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} />
  
    <label for="confirmPassword">Confirm Password</label>
    <input type="password" id="confirmPassword" bind:value={confirmPassword} />

    <br>
    <button on:click={handleRegister}>Register</button>  
    <br>
    <a  href={null} on:click={() => push('/login')}>Already a member?</a>
</form>
</main>

