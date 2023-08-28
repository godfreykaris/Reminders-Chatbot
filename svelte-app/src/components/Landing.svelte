<script>
  import {push} from 'svelte-spa-router'
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
  <button on:click={() => push('/login')}>Login</button>
  <button on:click={() => push('/register')}>Register</button>
  <button on:click={() => push('/edituser')}>EditUser</button>
  <button on:click={() => push('/deleteuser')}>DeleteUser</button>

  <button on:click={() => push('/addgoal')}>AddGoal</button>
  <button on:click={() => push('/editgoal')}>EditGoal</button>
  <button on:click={() => push('/deletegoal')}>DeleteGoal</button>

</div>
