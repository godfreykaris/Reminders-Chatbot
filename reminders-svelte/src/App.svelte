<script>
  import Router from 'svelte-spa-router'

  import Landing from './components/Landing.svelte';
  import Login from './components/Login.svelte';
  import Logout from './components/Logout.svelte';
  import Register from './components/Register.svelte';
  import Dashboard from './components/Dashboard.svelte';

  import Notfound from  './components/Notfound.svelte';


  const routes = {
    
    '/': Landing,

    '/login': Login,
    '/logout': Logout,

    '/register': Register,
    

    '/dashboard': Dashboard,


    '*' : Notfound,
}
  
</script>

<Router {routes}/>
