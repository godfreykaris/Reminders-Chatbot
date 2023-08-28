import { goto } from 'svelte-spa-router';

export function requireAuth() {
  const token = localStorage.getItem('authToken'); // Retrieve the authentication token

  if (!token) {
    // If the token is not present, redirect to the login page
    goto('/login');
  }
}
