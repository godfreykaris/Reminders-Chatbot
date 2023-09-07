<!-- Goals.svelte -->
<script>
  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';
  import {push} from 'svelte-spa-router';
  import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
  import { Button, Modal } from 'flowbite-svelte';

  import { writable } from 'svelte/store';
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
          // @ts-ignore
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

  function updateGoals(goal) {
       // Update the goals array to remove the deleted goal
    goals = goals.filter(g => g.id !== goal.id);
  }

  function handleGoalEdited(event) {
    const { editedGoal } = event.detail;
    // Update the corresponding goal in the goals array
    const editedIndex = goals.findIndex(goal => goal.id === editedGoal.id);
    if (editedIndex !== -1) {
      goals[editedIndex] = editedGoal;
    }
  }

  function handleGoalAdded(event) {
    // Retrieve the added goal from the event payload
    const addedGoal = event.detail.addedGoal;
    goals.push(addedGoal);
    alert(goals)
  }

  onMount(() => {
    fetchGoals(); // Fetch goals when the component is mounted
  });
</script>


<!-- Add Goal Modal -->
<Modal bind:open={isAddGoalModalOpen} size="xs" autoclose={false} class="max-w-sm">
  <AddGoalModal on:closeModal={fetchGoals} />
</Modal>


<!-- EditGoalModal component here -->
<Modal bind:open={isEditGoalModalOpen} size="xs" autoclose={false} class="max-w-sm">
  <EditGoalModal bind:selectedGoal={selectedGoal} on:goalEdited={handleGoalEdited}/>
</Modal>


<!-- DeleteGoalModal component here -->
<Modal bind:open={isDeleteGoalModalOpen} size="xs" autoclose={false} class="max-w-sm">
  <DeleteGoalModal {selectedGoal} {updateGoals}/>
</Modal>

<main class="container">
  <Button on:click={() => (isAddGoalModalOpen = true)} class="w-40 m-2">Add Goal</Button>


  {#if isLoading}
    <div class="flex items-center justify-center">
      <Circle2 size="64" />
    </div>
  {/if}

  {#if goals.length > 0}
  <Table hoverable={true} class="relative overflow-x-auto">
    <TableHead>
      <TableHeadCell>Goal Title</TableHeadCell>
      <TableHeadCell>Goal Description</TableHeadCell>
      <TableHeadCell>Time of Day</TableHeadCell>
      <TableHeadCell>Time Zone</TableHeadCell>
      <TableHeadCell>Contact Choice</TableHeadCell>
      <TableHeadCell>Report Frequency</TableHeadCell>
      <TableHeadCell>Actions</TableHeadCell>
    </TableHead>
    <TableBody>
      {#each goals as goal}
        <TableBodyRow>
          <TableBodyCell>{goal.goal_title}</TableBodyCell>
          <TableBodyCell>{goal.goal_description}</TableBodyCell>
          <TableBodyCell>{goal.time_of_day}</TableBodyCell>
          <TableBodyCell>{goal.time_zone}</TableBodyCell>
          <TableBodyCell>{goal.contact_choice}</TableBodyCell>
          <TableBodyCell>{goal.report_frequency}</TableBodyCell>
          <TableBodyCell>
            <Button on:click={() => selectGoal(goal, 'edit')}>Edit</Button>
            <Button on:click={() => selectGoal(goal, 'delete')}>Delete</Button>
          </TableBodyCell>
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
  
  {:else}
    <p>No goals fetched</p>
  {/if}  

</main>

  <style>
    main {
      text-align: center;
      padding: 1em;
      max-width: 240px;
      margin: 0 auto;
    }
  
  
      /* Default styles for the container */
  .container {
    width: 100%; /* Default width for screens less than or equal to 1000px */
    max-width: 1000px; /* Maximum width for screens less than or equal to 1000px */
    margin: 0 auto; /* Center the container horizontally */
  }
  
  /* Media query for screens greater than 1000px */
  @media (min-width: 1001px) {
    .container {
      width: 100%; /* Set width to 100% for screens greater than 1000px */
    }
  }
  
  /* Media query for screens between 601px and 1000px */
  @media (min-width: 601px) and (max-width: 1000px) {
    .container {
      width: 500px; /* Set width to 400px for screens between 601px and 1000px */
    }
  }
  
  /* Media query for screens between 201px and 600px */
  @media (min-width: 201px) and (max-width: 600px) {
    .container {
      width: 400px; /* Set width to 300px for screens between 201px and 600px */
    }
  }
  
  </style>

