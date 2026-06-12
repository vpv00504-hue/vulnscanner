export default function UploadBox({ setInput }) {

  const handleFile = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      setInput(event.target.result);
    };

    reader.readAsText(file);
  };

  return (
    <div className="upload">
      <input type="file" accept=".c,.txt" onChange={handleFile} />
    </div>
  );
}