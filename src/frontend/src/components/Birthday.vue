<template>
  <tr>
    <td>{{ name }}</td>
    <td>{{ day }}/{{ month }}/{{ year }}</td>
    <td>{{ currentAge }}</td>
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
    return {};
  },
  computed: {
    birthdate() {
      return new Date(
        this.month.toString() +
          '/' +
          this.day.toString() +
          '/' +
          this.year.toString()
      );
    },
    currentAge() {
      var ageDifMs = Date.now() - this.birthdate.getTime();
      var ageDate = new Date(ageDifMs);
      return Math.abs(ageDate.getUTCFullYear() - 1970);
    }
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
