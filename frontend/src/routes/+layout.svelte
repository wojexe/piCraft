<script lang="ts">
  import "normalize.css";

  import { SvelteToast } from "@zerodevx/svelte-toast";

  import Header from "@/components/header.svelte";
  import Footer from "@/components/footer.svelte";
</script>

<SvelteToast />

<Header />
<div class="content">
  <slot />
</div>
<Footer />

<style lang="scss">
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 2em;
    margin: 2em;
  }
</style>
