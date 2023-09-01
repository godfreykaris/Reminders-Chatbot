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
  <button on:click={() => push('/dashboard')}>Home</button>

  <hr/>

  <button on:click={() => push('/edituser')}>Edit User</button>
  <button on:click={() => push('/deleteuser')}>Delete User</button>

  <hr/>

  <button on:click={() => push('/addgoal')}>Add Goal</button>
  <button on:click={() => push('/editgoal')}>Edit Goal</button>
  <button on:click={() => push('/deletegoal')}>Delete Goal</button>
  
  <hr/>

  <button on:click={() => push('/viewgoals')}>View Goals</button>
  <button on:click={() => push('/viewreport')}>View Report</button>

  <hr/>


  <button on:click={() => push('/logout')}>Logout</button>

</div>