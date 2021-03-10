<template>
  <li>
    <h2>{{ name }}</h2>
    <button @click="toggleDetails">
      {{ detailsAreVisible ? 'Hide' : 'Show' }} Details
    </button>
    <ul v-if="detailsAreVisible">
      <li>
        <strong>Date of birth:</strong>
        {{ day }}/{{ month }}/{{ year }}
      </li>
    </ul>
    <button @click="$emit('delete', frontId)">Delete</button>
  </li>
</template>

<script>
export default {
  props: {
    frontId: {
      type: String,
      required: true,
    },
    id: {
      type: Number,
      required: false,
    },
    name: {
      type: String,
      required: true,
    },
    day: {
      type: Number,
      required: true,
    },
    month: {
      type: Number,
      required: true,
    },
    year: {
      type: Number,
      required: true
    },
  },
  emits: ['delete'],
  data() {
    return {
      detailsAreVisible: false,
    };
  },
  methods: {
    toggleDetails() {
      this.detailsAreVisible = !this.detailsAreVisible;
    },
  },
};
</script>
