import { Button } from "../../button";

const normalize=(text: string)=>{
  return text.replaceAll(/[$&+,:;=?@#|'"<>.^*()%!\s-]/g, '').toLocaleLowerCase()
}

const keywords=[
  'i dont have any',
  'я не знаю',
  'i dont know',
  'does not provide a specific',
].map(normalize);

console.log(normalize(' hello world yes'))


const callOperator=()=>{
  alert('Оператор подключается...')
}


export default function ChatCallOperator({ content }: { content: string }) {
  if(!content){
    return null;
  }
  const normContent=normalize(content)
  const showButton=keywords.some(keyword=>normContent.includes(keyword))
  if(showButton){
    return <Button variant="secondary" className="space-2" onClick={callOperator}>
      Перевести на оператора
    </Button>
  }
  return null
}
