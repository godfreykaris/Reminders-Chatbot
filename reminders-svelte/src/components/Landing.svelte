<script>
  import {push} from 'svelte-spa-router'
  import { Button} from 'flowbite-svelte';

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
  <h1>Reminders App</h1>
  <Button class="m-4" on:click={() => push('/login')}>Login</Button>
  <Button class="m-4" on:click={() => push('/register')}>Register</Button>

</div>
