import { Button } from "../../button";

const callOperator=()=>{
  alert('Оператор подключается...')
}

export default function ChatCallOperator({ content }: { content: string }) {
  return <Button variant="secondary" className="space-2" onClick={callOperator}>
    Перевести на оператора
  </Button>
}
