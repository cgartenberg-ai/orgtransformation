import { redirect } from "next/navigation";

export const metadata = {
  title: "Redirecting to Findings...",
};

export default function InsightsPage() {
  redirect("/findings");
}
