<script lang="ts">
  import { push } from "svelte-spa-router";
  
  // @ts-ignore
  import { onMount } from 'svelte';
  import { Circle2 } from 'svelte-loading-spinners';
  import { Section, Register } from 'flowbite-svelte-blocks';
  import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons'

  // @ts-ignore
  import { Button, Checkbox, Label, Input } from 'flowbite-svelte';
  
  import PhoneInput from './PhoneInput.svelte'

  import type {
    		E164Number,
    	
    } from 'svelte-tel-input/types';
    
	let value: E164Number | null;
  
  let isLoading = false;

  let name =   '' ;
  let email = '';
  let phone = '';
  let password = '';
  let confirmPassword = '';
  let error_message = ''; // Initialize response message variable
  let success_message = ''; // Initialize response message variable

  let showPassword = false;
  let showConfirmPassword = false;


  async function handleRegister() {
    // Scroll to the top of the page
    window.scrollTo({ top: 0, behavior: 'smooth' });

    success_message = "";
    error_message = "";
    isLoading = true;
    try {

      phone = value.toString();

      if( !phone || !name || !email || !password || !confirmPassword)
      {
        error_message = "Please fill in all the details.";
        success_message = "";
        isLoading = false;
        return;
      }

      // @ts-ignore
      let csrf = document.getElementsByName("csrf-token")[0].content;
      const response = await fetch(`/api/register`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf,
        }, 
        body: JSON.stringify({
          phone: value.toString(),
          name: name,          
          email: email,
          password: password,
          confirmPassword: confirmPassword
        }),
      });

      const data = await response.json();
      
      if (response.ok) 
      {

        // Registration successful
        alert('Registration successful.');
        success_message = data.message; // Set the error message from the response
        error_message = "";
        isLoading = false;
        push('/login');
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

  function togglePasswordVisibility() {
      showPassword = !showPassword;
  }

  function toggleConfirmNewPasswordVisibility() {
      showConfirmPassword = !showConfirmPassword;
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

<Section name="register" >
  <Register href="/">
    <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
      <form class="flex flex-col space-y-6" action="/">
        <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reminders  </h3>
        <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Create an account</h3>
        <!-- Show loading indicator while isLoading is true -->
        {#if isLoading}
          <div class="flex items-center justify-center">
            <Circle2 size="64" />
          </div>
        {/if}
        
        <!-- Display error or success message based on conditions -->
        {#if error_message}
          <p class="error-message">{error_message}</p>
        {:else if success_message}
          <p class="success-message">{success_message}</p>
        {/if}

        <Label class="space-y-2">
          <span>Name</span>
          <Input type="text" name="name" bind:value={name} placeholder="John Doe" class="border-1 border-black" required />
        </Label>
        <Label class="space-y-2">
          <span>Email</span>
          <Input type="email" name="email" bind:value={email} placeholder="name@company.com" class="border-1 border-black" required />
        </Label>

        <!-- Include the PhoneInput component -->
        <PhoneInput bind:value/>
      
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
        <Label class="space-y-2">
          <strong><span>Confirm Password</span></strong>
          <div class="relative">
            <Input type={showConfirmPassword ? 'text' : 'password'} name="confirm-password" bind:value={confirmPassword} placeholder="•••••" class="border-1 border-black focus:ring-blue-500 focus:border-blue-500" required />
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <span on:click={toggleConfirmNewPasswordVisibility} class="cursor-pointer absolute inset-y-0 right-0 flex items-center px-2">
                {#if showConfirmPassword}
                    <EyeOutline/>
                {:else}
                    <EyeSlashOutline/>
                {/if}
            </span>
          </div>
        </Label>
                        
        <Button on:click={handleRegister} class="w-full1">Create an account</Button>
        
        <div class="text-sm font-medium text-gray-500 dark:text-gray-300">
          Already have an account? <a href={null} class="font-medium text-primary-600 hover:underline dark:text-primary-500" on:click={() => push('/login')}>Login here</a>

        </div>
      </form>
    </div>
  </Register>
</Section>

