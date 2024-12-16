var parsedOutput;

function gameOver() {
  document.getElementById('message').innerHTML = "You lost";
  document.getElementById('myHP').innerHTML = "0";
  setTimeout(() => {
    window.location.href = "/";
  }, 2000);
}

function updateStats() {
  if (typeof parsedOutput === "undefined") return;
  if (parsedOutput == "0") gameOver();
  document.getElementById('message').innerHTML = parsedOutput.message[0];
  document.getElementById('myHP').innerHTML = parsedOutput.allyHP;
  document.getElementById('apHP').innerHTML = parsedOutput.opponentHP;
  if(parsedOutput.message[0] == "GAME OVER") gameOver();
  if (parsedOutput.message.length > 1) {
    parsedOutput.message.shift();
  }
}

function useMule(mule){
  if(typeof parsedOutput !== 'undefined' && parsedOutput.message.length > 1){
    alert("You can't move yet");
    return;
  }
  fetch('/battle?selectedMove=' + mule)
    .then(response => {
      if (response.status === 200) {
        return response.text();
      } else {
        throw new Error('Request failed with status ' + response.status);
      }
    })
    .then(output => {
      parsedOutput = JSON.parse(output);
      if(parseInt(parsedOutput.allyHP) > 100) parsedOutput.allyHP = 100;
      if(parseInt(parsedOutput.opponentHP) > 100) parsedOutput.opponentHP = 100;
      updateStats();
    })
    .catch(error => {
      console.error(error);
    });

}