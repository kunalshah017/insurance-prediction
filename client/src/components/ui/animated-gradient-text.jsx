import { cn } from "../../utils";

export default function AnimatedGradientText({
  children,
  className
}) {
  return (
    <div
      className={cn(
        "relative mx-auto flex max-w-fit flex-row items-center justify-center text-transparent bg-clip-text bg-gradient-to-r from-[#ffaa40] via-[#9c40ff] to-[#ffaa40] animate-text",
        className
      )}
    >
      <style jsx>{`
        @keyframes text-gradient {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }
        .animate-text {
          background-size: 200% 200%;
          animation: text-gradient 3s ease infinite;
        }
      `}</style>
      {children}
    </div>
  );
}
