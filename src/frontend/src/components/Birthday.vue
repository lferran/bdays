<template>
  <tr>
    <td>{{ name }}</td>
    <td>{{ day }}/{{ month }}/{{ year }}</td>
    <td><button @click="deleteBday(id)">Delete</button></td>
  </tr>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: false
    },
    name: {
      type: String,
      required: true
    },
    day: {
      type: Number,
      required: true
    },
    month: {
      type: Number,
      required: true
    },
    year: {
      type: Number,
      required: true
    }
  },
  emits: ['delete'],
  data() {
    return {
    };
  },
  methods: {
    deleteBday(id) {
      if (confirm('Are you sure?')) {
        this.$emit('delete', id);
      }
    }
  }
};
</script>
