<script lang="ts">
    import { Circle2 } from 'svelte-loading-spinners';
    // @ts-ignore
    import { createEventDispatcher } from 'svelte';

    // @ts-ignore
    import { Button, Checkbox, Label, Input } from 'flowbite-svelte';

    import PhoneInput from './PhoneInput.svelte'

    import type {
          E164Number,

      } from 'svelte-tel-input/types';

    let value: E164Number | null;

    let email = '';
    let phone_number = '';
    let isLoading = false;

    let error_message = ''; // Initialize response message variable
    let success_message = ''; // Initialize response message variable


    

    async function resetPassword() {
        if (!validate_email(email)) {
            alert('Invalid email format. Please enter a valid email address.');
            return;
        }

        phone_number = value.toString();
     
        if (!phone_number) {
            alert('Invalid phone number. Please enter a valid phone number.');
            return;
        }

        isLoading = true;

        // @ts-ignore
        let csrf = document.getElementsByName("csrf-token")[0].content;

        const response = await fetch('/api/reset_password', {
            method: "POST",
            credentials: "same-origin",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf,
            },
            body: JSON.stringify({ email, phone_number }),
        });

      

        if (response.ok) {
            alert('A new password has been sent to your email, check your inbox');
            success_message = "Password reset successful.";
            error_message = '';
        } else {
            error_message = 'Password reset failed, please try again later';
            success_message = '';
        }

        isLoading = false;
                
    }

    function validate_email(email) {
        const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return email_regex.test(email);
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

<form class="flex flex-col space-y-6 " action="#">
  <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reminders  </h3>
  <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Reset Password</h3>
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
    <span>Email</span>
    <Input type="email" name="email" bind:value={email} placeholder="name@company.com" class="border-1 border-black" required />
  </Label>
  <!-- Include the PhoneInput component -->
  <PhoneInput bind:value/>
  <Button on:click={resetPassword} class="w-full1">Reset Password</Button>
</form>