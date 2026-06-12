export default function Message({ role, text }) {
  return (
    <div className={`msg ${role}`}>
      <pre>{text}</pre>
    </div>
  );
}