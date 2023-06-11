<script lang="ts">
  import type { ModificationParam } from "@/lib/api";

  export let param: ModificationParam;

  const dynamicType = (node: HTMLInputElement) => {
    node.type = param.type;
  }
</script>

<div class="modificationParam">
  <label for={`param${param.name}`}>{param.display}</label>
  <input id={`param${param.name}`} use:dynamicType bind:value={param.value} />
</div>

<style lang="scss">
  .modificationParam {
    display: flex;
    flex-direction: column;
    label {
      font-size: 0.8em;
      font-weight: 500;
    }
    input {
      width: 12ch;
      padding: 0.5ch 1ch;
      border: none;

      border-radius: 1rem;
    }
  }
</style>
