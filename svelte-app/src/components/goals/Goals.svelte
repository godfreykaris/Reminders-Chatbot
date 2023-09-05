<!-- Goals.svelte -->
<script>
  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';
  import {push} from 'svelte-spa-router';

  import AddGoalModal from './AddGoalModal.svelte';
  import EditGoalModal from './EditGoalModal.svelte'; 
  import DeleteGoalModal from './DeleteGoalModal.svelte';

  let isAddGoalModalOpen = false;
  let isEditGoalModalOpen = false; 
  let isDeleteGoalModalOpen = false; 

  let isLoading = false;

  let goals = [];  
  let selectedGoal = null;

  let error_message = '';
  let success_message = '';

  // Simulate an API response with test data
  goals = [ ];

  let timezones = [];

  function openAddGoalModal() {
      isAddGoalModalOpen = true;
    }


  async function selectGoal(goal, action) {
    selectedGoal = goal;
    if(action === 'edit')
    {
      isEditGoalModalOpen = true;
      isDeleteGoalModalOpen = false;
    }
    else
    {
      isEditGoalModalOpen =false;
      isDeleteGoalModalOpen = true;
    }
      
  }

  

  async function fetchGoals() {

    isLoading = true;

    const response = await fetch(`/api/get_goals`, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'Accept': 'application/json',
          'X-CSRFToken': document.getElementsByName("csrf-token")[0].content,
        },
      });

      if (response.status === 200) {
        goals = await response.json();
        error_message = '';
        success_message = 'Goals fetched successfully';
        isLoading = false;
      } else if (response.status === 401) 
      {
        // Redirect to the login page when Unauthorized (401) status is received
        push('/login'); // Replace '/login' with your actual login page URL

      } else {
        error_message = "An error occurred trying to fetch goals";
        success_message = '';
        isLoading = false;
      }
  }

  onMount(() => {
    fetchGoals(); // Fetch goals when the component is mounted
  });
</script>


<!-- Add Goal Modal -->
{#if isAddGoalModalOpen}
  <AddGoalModal on:closeModal={() => (isAddGoalModalOpen = false)} />
{/if}

<!-- EditGoalModal component here -->
{#if isEditGoalModalOpen && selectedGoal !== null}
  <EditGoalModal selectedGoal={selectedGoal} on:closeModal={() => {isEditGoalModalOpen = false; selectedGoal = null; }} />
{/if}

<!-- EditGoalModal component here -->
{#if isDeleteGoalModalOpen && selectedGoal !== null}
  <DeleteGoalModal selectedGoal={selectedGoal} on:closeModal={() => {isDeleteGoalModalOpen = false; selectedGoal = null; }} />
{/if}


<div class="goals-tab">
  <h1>Goals</h1>
  <button on:click={() => openAddGoalModal()}>Add Goal</button>


  {#if isLoading}
    <div class="center-container">
      <Circle2 size="64" />
    </div>
  {/if}

  {#if goals.length > 0}
    <table>
      <thead>
        <tr>
          <th>Goal Title</th>
          <th>Goal Description</th>
          <th>Time of Day</th>
          <th>Time Zone</th>
          <th>Contact Choice</th>
          <th>Report Frequency</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#each goals as goal}
          <tr>
            <td>{goal.goal_title}</td>
            <td>{goal.goal_description}</td>
            <td>{goal.time_of_day}</td>
            <td>{goal.time_zone}</td>
            <td>{goal.contact_choice}</td>
            <td>{goal.report_frequency}</td>
            <td>
              <button on:click={() => selectGoal(goal, 'edit')}>Edit</button>
              <button on:click={() => selectGoal(goal, 'delete')}>Delete</button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <p>No goals fetched</p>
  {/if}


  
</div>

<style>
  .goals-tab {
    text-align: center;
    padding: 1em;
    max-width: 600px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }

  button {
    margin-right: 5px;
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
    flex-direction: column; /* Center vertically */
    justify-content: center; /* Center vertically */
    align-items: center; /* Center horizontally */
  }
</style>
