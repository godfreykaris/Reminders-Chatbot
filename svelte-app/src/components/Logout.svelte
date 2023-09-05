<script>
  import {push} from 'svelte-spa-router';

  import { onMount } from 'svelte';

  import { Circle2 } from 'svelte-loading-spinners';

  let isLoading = false;

  async function logout() {

    isLoading = true;

    await fetch('/api/logout', {
      method: 'GET',
      credentials: 'same-origin' // Include cookies in the request
    })
    .then(response => response.json())
    .then(data => {
      // Handle the response data
      if (data.logout) {
        // Redirect or perform any necessary action
        push('/login'); // Redirect to the login page
      } else {
        console.log('Logout failed');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
    .finally(() => {
      isLoading = false;
    });
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
  
</style>

<div class='center-container'>
  <h1>Logout</h1>
  <button on:click={logout}>Logout</button>

  {#if isLoading}
    <Circle2 size="64" />
  {/if}

</div>



