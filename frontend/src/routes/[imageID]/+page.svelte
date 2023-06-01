<script lang="ts">
  import type { PageData } from "./$types";
  //@ts-ignore
  export let data: PageData;
  $: console.log(data)
</script>

<h1>{data.title}</h1>