<script lang="ts">
  export let param: any;

  const paramID = `param-${param.id}`;

  const boundedValue = (val: number | null, min: number, max: number) => {
    if (val == null) return val;

    if (val < min) return min;
    if (val > max) return max;
    return val;
  };
</script>

{#if param.type === "text"}
  <div class="modificationParam">
    <label for={paramID}>{param.display}</label>
    <input id={paramID} placeholder={param.defaultValue} type="text" bind:value={param.value} />
  </div>
{:else if param.type === "number"}
  <div class="modificationParam">
    <label for={paramID}>{param.display}</label>
    <input
      id={paramID}
      placeholder={param.defaultValue}
      type="number"
      min={param.min}
      max={param.max}
      on:change={() => (param.value = boundedValue(param.value, param.min, param.max))}
      bind:value={param.value}
    />
  </div>
{:else if param.type === "select"}
  <div class="modificationParam">
    <label for={paramID}>{param.display}</label>
    <select id={paramID} bind:value={param.value}>
      {#each param.selections as option}
        <option value={option}>{option}</option>
      {/each}
    </select>
  </div>
{/if}

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
