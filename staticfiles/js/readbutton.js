const expandableButtons = document.querySelectorAll('[data-expand-button]')

expandableButtons.forEach(button => {
  button.addEventListener('click', toggleText)
  setExpandButtonText(button)
})

function toggleText(e) {
  const expandableElement = e.target.closest('[data-expandable]')
  expandableElement.classList.toggle('expanded')
  setExpandButtonText(e.target)
}

function setExpandButtonText(button) {
  const expandableElement = button.closest('[data-expandable]')
  const expanded = expandableElement.classList.contains('expanded')
  button.innerText = expanded ? 'Read Less' : 'Read More'
}