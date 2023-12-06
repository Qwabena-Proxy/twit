const dropBtn= document.getElementById('dropBtn');
const userBtn= document.getElementById('useroptbtn');
const mobileMenu= document.getElementById('mobile-menu');
const userMenu= document.getElementById('userdropdown');
const erroralertbtn= document.getElementById('closebtn');
const alert= document.getElementById('alert');

dropBtn.addEventListener('click', () => {
  if(mobileMenu.classList.contains('hidden')){
    mobileMenu.classList.remove('hidden');
  }else{
    mobileMenu.classList.add('hidden');
  }
});

userBtn.addEventListener('click', () => {
    if(userMenu.classList.contains('hidden')){
      userMenu.classList.remove('hidden');
    }else{
      userMenu.classList.add('hidden');
    }
  });

erroralertbtn.addEventListener('click', () => {
    if(alert.classList.contains('hidden')){
      alert.classList.remove('hidden');
    }else{
      alert.classList.add('hidden');
    }
  });