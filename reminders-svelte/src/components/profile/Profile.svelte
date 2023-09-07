<!-- Profile.svelte -->
<script>
    import { onMount } from 'svelte';
    import { Circle2 } from 'svelte-loading-spinners';
    import { push } from 'svelte-spa-router';

    import { Button, Modal } from 'flowbite-svelte';

    import EditUserModal from './EditUserModal.svelte';
    import ChangePasswordModal from './ChangePasswordModal.svelte';

    let isEditUserModalOpen = false;
    let isChangePasswordModalOpen = false;

      
    let isLoading = false;
  
    let user = {
      name: '', // Initialize with empty values or defaults
      email: '',
      phone: '',
    };

    // @ts-ignore
    let userDetails = [
      { label: 'Name', value: user.name },
      { label: 'Email', value: user.email },
      { label: 'Phone', value: user.phone }
    ]
  
    let error_message = '';
    let success_message = '';

   
      
    async function fetchUser() {
      isLoading = true;
      // Fetch the current user's data
      const response = await fetch(`/api/user_data`, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'Accept': 'application/json',
          // @ts-ignore
          'X-CSRFToken': document.getElementsByName("csrf-token")[0].content,
        },
      });
  
      if (response.status === 200) {
        let data = await response.json();
        user = data.user_info;
      }
      else if (response.status === 401) 
      {
        // Redirect to the login page when Unauthorized (401) status is received
        push('/login'); // Replace '/login' with your actual login page URL

      }
      else 
      {
        error_message = "An error occurred trying to fetch your data.";
        success_message = '';
        isLoading = false;
        location.reload();

      }

      isLoading = false;

    }

    // Add a reactive statement to listen for changes in editUserModal
   // @ts-ignore
     $: {
      if (!isEditUserModalOpen) {
        fetchUser();
      }
    }

   // @ts-ignore
     $: {
      if (!isChangePasswordModalOpen) {
        fetchUser();
      }
    }
  
    async function logout() {
      isLoading = true;
      await fetch('/api/logout', {
        method: 'GET',
        credentials: 'same-origin',
      })
        .then(response => response.json())
        .then(data => {
          if (data.logout) {
            push('/login'); // Redirect to the login page on successful logout
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
      fetchUser(); // Fetch user data when the component is mounted
    });
  </script>

<!-- Edit User Modal -->
<Modal bind:open={isEditUserModalOpen} size="xs" autoclose={false} class="w-full max-w-sm">
  <EditUserModal editedUser={user} on:closeModal={() => { fetchUser(); isEditUserModalOpen = false; }}/>
</Modal>

<!--Change password modal-->
<Modal bind:open={isChangePasswordModalOpen} size="xs" autoclose={false} class="w-full max-w-sm">
  <ChangePasswordModal />
</Modal>


<main class="center-container">

{#if error_message != ''}
  <p class="error-message">{error_message}</p>
{:else if success_message != ''}
  <p class="success-message">{success_message}</p>
{/if}

{#if isLoading}
  <div class="center-container">
    <Circle2 size="64" />
  </div>
{:else}
  <p class="text-black"><strong>Name:</strong> <br>{user.name}</p>
  <p class="text-black"><strong>Email:</strong> <br>{user.email}</p>
  <p class="text-black"><strong>Phone:</strong> <br>{user.phone}</p>


  <hr />

  <Button on:click={() => (isChangePasswordModalOpen = true)} class="w-40 m-2">Change Password</Button>

  <Button on:click={() => (isEditUserModalOpen = true)} class="w-40 m-2">Edit Profile</Button>
  <Button on:click={logout} class="w-40 m-2">Logout</Button>
{/if}



</main>

<style>
main {
  text-align: center;
  padding: 1em;
  max-width: 240px;
  margin: 0 auto;
}

.center-container {
        display: flex;
        flex-direction: column; /* Center vertically */
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
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

/* Add your custom styles here for the Profile tab */
</style>
  