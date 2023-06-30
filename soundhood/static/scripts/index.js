let activeIndex = 0;
const groups = document.getElementsByClassName("user-card");
console.log('Hi from script')

const handleLoveClick = () => {
  const nextIndex = activeIndex + 1 <= groups.length - 1 ? activeIndex + 1 : 0;
  const currentGroup = document.querySelector(`[data-index="${activeIndex}"]`),
    nextGroup = document.querySelector(`[data-index="${nextIndex}"]`);

  // Active group becomes after
  
  currentGroup.dataset.status = "after";

  // Next group becomes active
  
  nextGroup.dataset.status = "active";

  activeIndex = nextIndex;
}

const redirectToUserProfile = (userId) => {
  window.location.href = 'http://127.0.0.1:5000/user_profile/' + userId;
}
