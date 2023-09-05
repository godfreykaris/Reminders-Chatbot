<!-- Tabs.svelte -->
<script>
  import Profile from './profile/Profile.svelte'
  import Goals from './goals/Goals.svelte'
  import ViewReport from './reports/ViewReport.svelte';

  let activeTab = 'goals'; // Default to the 'goals' tab

  function switchTab(tab) {
    activeTab = tab;
  }
</script>

<style>
  .tab-container {
    display: flex;
    justify-content: center;
  }

  .tab-list {
    display: flex;
    list-style: none;
    padding: 0;
  }

  .tab-list button {
    background-color: #f2f2f2;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 0 5px;
    padding: 5px 10px;
  }

  .tab-list button.active {
    background-color: #007BFF; /* Change to your desired color for the active tab */
    color: white;
  }
</style>

<div class="tab-container">
  <ul class="tab-list">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <li><button class={activeTab === 'profile' ? 'active' : ''} on:click={() => switchTab('profile')}>Profile</button></li>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <li><button class={activeTab === 'goals' ? 'active' : ''} on:click={() => switchTab('goals')}>Goals</button></li>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <li><button class={activeTab === 'reports' ? 'active' : ''} on:click={() => switchTab('reports')}>Reports</button></li>
  </ul>
</div>

<!-- Display the content of the selected tab -->
<div class="tab-content">
  {#if activeTab === 'profile'}
    <Profile />
  {/if}
  {#if activeTab === 'goals'}
    <Goals />
  {/if}
  {#if activeTab === 'reports'}
    <ViewReport />
  {/if}
</div>
