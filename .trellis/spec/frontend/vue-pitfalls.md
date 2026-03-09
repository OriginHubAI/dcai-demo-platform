# Vue 3 Pitfalls & Common Mistakes

> Avoid these common errors when writing Vue 3 Composition API code.

---

## 1. the `.value` Trap

When using `ref()`, you **must** use `.value` to read or write the value inside JavaScript blocks (`<script setup>`, composables). 

Inside the `<template>`, Vue automatically unwraps the ref, so you **do not** use `.value` there.

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
const data = ref([])

// BAD: Mutating the ref object itself or forgetting .value
count = 1 // Error: Assignment to constant variable
data.push('item') // Error: data is a RefImpl, doesn't have .push()

// GOOD: Mutating the inner value
count.value = 1
data.value.push('item')
</script>

<template>
  <!-- GOOD: Vue unwraps automatically in template -->
  <div>Count is: {{ count }}</div>
  
  <!-- BAD: Dont use .value in template -->
  <div>Count is: {{ count.value }}</div>
</template>
```

---

## 2. Losing Reactivity via Destructuring

### Destructuring Props

If you destructure `props` directly, the extracted variables lose reactivity. They will not update if the parent changes the prop.

```vue
<script setup>
import { toRefs } from 'vue'

const props = defineProps({
  title: String,
  user: Object
})

// BAD: title is now a static string
const { title } = props 

// GOOD: Access via props object
console.log(props.title) 

// GOOD: Use toRefs to keep reactivity if destructuring is necessary
const { title, user } = toRefs(props)
console.log(title.value) 
</script>
```

### Destructuring Composables

When a composable returns reactive state (like `reactive({})`), destructuring it drops the reactivity:

```javascript
// BAD 
const { user, status } = reactive({ user: null, status: 'loading' }) // Lost reactivity

// GOOD: Use toRefs to convert a reactive object properties back into refs
const state = reactive({ user: null, status: 'loading' })
const { user, status } = toRefs(state) // Retains reactivity
```

*Note: Composables that return a plain object containing `refs` (e.g. `{ user: ref(null) }`) can be destructured safely without `toRefs`.*

---

## 3. Misusing `watch` vs `watchEffect`

- **`watch`**: Explicitly specify which sources to observe. Ideal when you only want the callback to trigger when a specific input changes, and you need access to the `oldValue` and `newValue`.
- **`watchEffect`**: Automatically discovers dependencies based on what reactive properties are read synchronously inside the callback. It runs immediately upon creation.

```javascript
const id = ref(1)

// BAD: Doesn't track anything because 'id.value' is passed as a primitive, not a reactive source
watch(id.value, (newVal) => fetch(newVal)) 

// GOOD: Track the ref itself
watch(id, (newVal) => fetch(newVal))

// GOOD: Track a getter if watching properties of reactive objects
const state = reactive({ count: 0 })
watch(() => state.count, (newVal) => console.log(newVal))
```

---

## 4. Mutating Props

Child components should **never** directly mutate properties passed to them via props. Data flow must be one-way: Down from Parent, Up via Events.

```vue
<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

// BAD: Mutating prop directly
const updateText = (newText) => {
  props.modelValue = newText // Error! Props are readonly
}

// GOOD: Emit update event to let parent mutate
const updateText = (newText) => {
  emit('update:modelValue', newText)
}
</script>
```

If you are binding a prop to a child component (e.g. `v-model`), Vue 3 supports this out of the box using `modelValue` and `@update:modelValue`. You can further simplify this using the `computed` property with a setter:

```vue
<script setup>
import { computed } from 'vue'
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})
</script>

<template>
  <input v-model="internalValue" />
</template>
```

---

## 5. Forgetting to Clean Up Event Listeners

If you attach event listeners to `window` or `document` manually during `onMounted`, you must clean them up in `onUnmounted` or `onBeforeUnmount`. Failing to do so creates memory leaks.

```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'

const handleScroll = () => { /* ... */ }

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

// VITAL: Clean up!
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
```

---

**Language**: All documentation must be written in **English**.
