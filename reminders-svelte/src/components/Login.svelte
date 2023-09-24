<script>
  import {push} from 'svelte-spa-router';

  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';
  import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons'
  import { Section, Register } from 'flowbite-svelte-blocks';
  import { Button, Modal,  Label, Input } from 'flowbite-svelte';

  import ForgotPassword from './ForgotPassword.svelte';

  let forgotPasswordModal = false;

  let isLoading = false;
  let showPassword = false;

  let username = '';
  let password = '';
  let errorMessage = ''; // Initialize response error message variable
  let successMessage = '';
  
  // Function to handle login
  async function handleLogin() {
    isLoading = true;
    errorMessage = '';
    successMessage = '';
    try {

      if(!username || !password)
      {
        errorMessage = "Please fill in all the details.";
        successMessage = '';
        isLoading = false;
        return;
      }

      // @ts-ignore
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
        successMessage  = data.message;
        errorMessage = '';
        isLoading = false;
        push('/dashboard') // Redirect to the dashboard
      } else if (response.status === 401) 
      {
        // Authentication failed
        errorMessage = 'Authentication failed. Please check your credentials.';
        successMessage = ''
        isLoading = false;
      } 
      else {
        errorMessage = "An error occurred while trying to log in. Please try again.";
        successMessage = ''
        isLoading = false;
      }
      
    }
    catch (error) 
     {
      console.error('Error:', error);
      errorMessage = 'An error occurred while trying to log in. Please try again.';
      successMessage = '';
      alert(errorMessage);
      location.reload();
      isLoading = false;
    }
  }
  onMount(() => {            
            // Reset isLoading state when the component is mounted
            isLoading = false;
          });
        

   
  function togglePasswordVisibility() {
        showPassword = !showPassword;
      }

</script>

<style>
  
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


<Modal bind:open={forgotPasswordModal} size="xs" autoclose={false} class="w-full h-2 max-w-sm">
  <ForgotPassword />
</Modal>
  
<Section name="login">
  <Register href="/">
    <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
      <form class="flex flex-col space-y-6" action="/">
        <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reminders</h3>
        <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Login</h3>
        
        {#if errorMessage}
          <p class='error-message'>{errorMessage}</p>
        {:else if successMessage}
          <p class='success-message'>{successMessage}</p>
        {/if}

        {#if isLoading}
          <div class="flex items-center justify-center">
            <Circle2 size="64" />
          </div>
        {/if}

        <Label class="space-y-2">
          <span>Your email or phone</span>
          <!-- Bind 'username' variable to the value of the input -->
          <Input class="border-1 border-black" type="text" name="username" bind:value={username} placeholder="email or phone number" required />
        </Label>
        <Label class="space-y-2">
            <strong><span>Password</span></strong>
            <div class="relative">
                <Input type={showPassword ? 'text' : 'password'} name="password" bind:value={password} placeholder="•••••" class="border-1 border-black focus:ring-blue-500 focus:border-blue-500" required />            
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <span on:click={togglePasswordVisibility} class="cursor-pointer absolute inset-y-0 right-0 flex items-center px-2">
                    {#if showPassword}
                        <EyeOutline/>
                    {:else}
                        <EyeSlashOutline/>
                    {/if}
                </span>
            </div>
        </Label>
        <div class="flex items-start">
          <a href={null} on:click={() => (forgotPasswordModal = true)} class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500">Forgot password?</a>
        </div>
        
        <!-- Trigger the 'handleLogin' function when the button is clicked -->
        <Button on:click={handleLogin} class="w-full1">Sign in</Button>
        <p class="text-sm font-light text-gray-500 dark:text-gray-400">
          Don’t have an account yet? <a href={null} class="font-medium text-primary-600 hover:underline dark:text-primary-500" on:click={() => push('/register')}>Sign up</a>
        </p>
      </form>
    </div>
  </Register>
</Section>