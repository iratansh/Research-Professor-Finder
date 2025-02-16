const researchIcons = ["📖", "💻", "📜", "📊", "💡", "🖊️"];

export default function FloatingIcons(){
  const icons = Array.from({ length: 10 }).map((_, index) => {
    const randomX = Math.random() * 100;
    const randomY = Math.random() * 100;
    const randomDuration = Math.random() * 10 + 5;

    return (
      <span
        key={index}
        className="icon"
        style={{
          left: `${randomX}vw`,
          top: `${randomY}vh`,
          animationDuration: `${randomDuration}s`,
          fontSize: "2rem",
        }}
      >
        {researchIcons[index % researchIcons.length]}
      </span>
    );
  });

  return <div className="research-bg">{icons}</div>;
};