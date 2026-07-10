"""📧 Automated Email Sender — GUI Edition"""

import threading
import time
import customtkinter as ctk
from tkinter import messagebox

# ==================================================================
# ============  ORIGINAL BACKEND CODE (LOGIC UNCHANGED)  ===========
# ==================================================================
import smtplib
from email.message import EmailMessage


def serv(server):
    
    server.login('hdeep89977@gmail.com', 'enter_your_password')


def send_bulk_emails(receiver_email, subject, message_body,
                      num_emails, delay, progress_callback,
                      stop_event, done_callback):
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)   
        server.starttls()                                

        serv(server)                                     

        msg = EmailMessage()
        msg['From'] = "hdeep89977@gmail.com"               
        msg['To'] = receiver_email          
        msg['subject'] = subject            

        msg.set_content(message_body)       

        for i in range(num_emails):         
            if stop_event.is_set():        
                break

            server.sendmail(                
                msg['From'],
                msg['To'],
                msg.as_string()
            )
            print(f"Email {i + 1} sent")    

            progress_callback(i + 1, num_emails)  

            if i + 1 < num_emails:
                time.sleep(delay)           

        server.quit()                       
        done_callback(True, None, stop_event.is_set())
    except Exception as e:
        done_callback(False, str(e), False)


# ==================================================================
# ==========================  GUI LAYER  ============================
# ==================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#----default-message-to-send-reciever---------

DEFAULT_MESSAGE = """Hello,

This is a test email sent using my Python Automated Email Sender project.

Regards,
Harmandeep"""


class EmailSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📧 Automated Email Sender")
        self.geometry("620x700")
        self.minsize(600, 680)
        self.resizable(False, False)
        self.configure(fg_color="#161C2B")

        
        self.update_idletasks()
        w, h = 620, 700
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.stop_event = threading.Event()
        self.sending_thread = None

        self._build_ui()

    # -------------------- UI CONSTRUCTION --------------------
    def _build_ui(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=16, pady=12)

        # Title
        title = ctk.CTkLabel(
            main, text="📧 Automated Email Sender",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4FD1C5"
        )
        title.pack(pady=(0, 12))

        # ---------- Email Details Card ----------
        details_card = ctk.CTkFrame(main, corner_radius=14, fg_color="#1E1E2E")
        details_card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(details_card, text="Receiver Email",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#A78BFA").pack(anchor="w", padx=14, pady=(12, 2))
        self.receiver_entry = ctk.CTkEntry(
            details_card, placeholder_text="example@gmail.com",
            height=34, corner_radius=10
        )
        self.receiver_entry.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkLabel(details_card, text="Subject",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#A78BFA").pack(anchor="w", padx=14, pady=(0, 2))
        self.subject_entry = ctk.CTkEntry(
            details_card, height=34, corner_radius=10
        )
        self.subject_entry.insert(0, "Hello from Python Email Sender")
        self.subject_entry.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkLabel(details_card, text="Message",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#A78BFA").pack(anchor="w", padx=14, pady=(0, 2))
        self.message_box = ctk.CTkTextbox(
            details_card, height=110, corner_radius=10
        )
        self.message_box.insert("1.0", DEFAULT_MESSAGE)
        self.message_box.pack(fill="x", padx=14, pady=(0, 14))

        # ---------- Bulk Settings Card ----------
        bulk_card = ctk.CTkFrame(main, corner_radius=14, fg_color="#1E1E2E")
        bulk_card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(bulk_card, text="⚙️  Bulk Email Settings",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#F6AD55").pack(anchor="w", padx=14, pady=(12, 8))

        row = ctk.CTkFrame(bulk_card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 14))
        row.grid_columnconfigure((0, 1), weight=1)

        col1 = ctk.CTkFrame(row, fg_color="transparent")
        col1.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkLabel(col1, text="Number of Emails",
                     font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.num_emails_entry = ctk.CTkEntry(col1, height=32, corner_radius=10)
        self.num_emails_entry.insert(0, "10")
        self.num_emails_entry.pack(fill="x", pady=(2, 0))

        col2 = ctk.CTkFrame(row, fg_color="transparent")
        col2.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        ctk.CTkLabel(col2, text="Delay (seconds)",
                     font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.delay_entry = ctk.CTkEntry(col2, height=32, corner_radius=10)
        self.delay_entry.insert(0, "6")
        self.delay_entry.pack(fill="x", pady=(2, 0))

        # ---------- Progress Card ----------
        progress_card = ctk.CTkFrame(main, corner_radius=14, fg_color="#1E1E2E")
        progress_card.pack(fill="x", pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(
            progress_card, height=16, corner_radius=8,
            progress_color="#4FD1C5"
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=14, pady=(14, 6))

        self.counter_label = ctk.CTkLabel(
            progress_card, text="0/0 Emails Sent",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.counter_label.pack(pady=(0, 12))

        # ---------- Buttons ----------
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(4, 0))
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.send_btn = ctk.CTkButton(
            btn_frame, text="🚀 Send Email", height=40, corner_radius=12,
            fg_color="#22C55E", hover_color="#16A34A",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_send
        )
        self.send_btn.grid(row=0, column=0, padx=4, sticky="ew")

        self.clear_btn = ctk.CTkButton(
            btn_frame, text="🧹 Clear", height=40, corner_radius=12,
            fg_color="#3B82F6", hover_color="#2563EB",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_clear
        )
        self.clear_btn.grid(row=0, column=1, padx=4, sticky="ew")

        self.stop_btn = ctk.CTkButton(
            btn_frame, text="⏹ Stop", height=40, corner_radius=12,
            fg_color="#F59E0B", hover_color="#D97706",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_stop
        )
        self.stop_btn.grid(row=0, column=2, padx=4, sticky="ew")

        self.exit_btn = ctk.CTkButton(
            btn_frame, text="❌ Exit", height=40, corner_radius=12,
            fg_color="#EF4444", hover_color="#DC2626",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_exit
        )
        self.exit_btn.grid(row=0, column=3, padx=4, sticky="ew")

        # Status footer
        self.status_label = ctk.CTkLabel(
            main, text="Ready.", font=ctk.CTkFont(size=11),
            text_color="#9CA3AF"
        )
        self.status_label.pack(pady=(10, 0))

    # -------------------- VALIDATION --------------------
    def _validate_inputs(self):
        receiver = self.receiver_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", "end").strip()

        if not receiver or "@" not in receiver:
            messagebox.showerror("Invalid Input", "Please enter a valid receiver email.")
            return None
        if not subject:
            messagebox.showerror("Invalid Input", "Subject cannot be empty.")
            return None
        if not message:
            messagebox.showerror("Invalid Input", "Message cannot be empty.")
            return None

        try:
            num_emails = int(self.num_emails_entry.get().strip())
            if num_emails <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of Emails must be a positive integer.")
            return None

        try:
            delay = float(self.delay_entry.get().strip())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Delay must be a non-negative number.")
            return None

        return receiver, subject, message, num_emails, delay

    # -------------------- BUTTON HANDLERS --------------------
    def on_send(self):
        if self.sending_thread and self.sending_thread.is_alive():
            return  # already sending

        inputs = self._validate_inputs()
        if not inputs:
            return
        receiver, subject, message, num_emails, delay = inputs

        self.stop_event.clear()
        self.progress_bar.set(0)
        self.counter_label.configure(text=f"0/{num_emails} Emails Sent")
        self.status_label.configure(text="Sending... please wait.", text_color="#4FD1C5")
        self.send_btn.configure(state="disabled")

        
        self.sending_thread = threading.Thread(
            target=send_bulk_emails,
            args=(receiver, subject, message, num_emails, delay,
                  self._on_progress, self.stop_event, self._on_done),
            daemon=True
        )
        self.sending_thread.start()

    def on_clear(self):
        self.receiver_entry.delete(0, "end")
        self.subject_entry.delete(0, "end")
        self.subject_entry.insert(0, "Hello from Python Email Sender")
        self.message_box.delete("1.0", "end")
        self.message_box.insert("1.0", DEFAULT_MESSAGE)
        self.num_emails_entry.delete(0, "end")
        self.num_emails_entry.insert(0, "10")
        self.delay_entry.delete(0, "end")
        self.delay_entry.insert(0, "6")
        self.progress_bar.set(0)
        self.counter_label.configure(text="0/0 Emails Sent")
        self.status_label.configure(text="Cleared.", text_color="#9CA3AF")

    def on_stop(self):
        if self.sending_thread and self.sending_thread.is_alive():
            self.stop_event.set()
            self.status_label.configure(text="Stopping after current email...", text_color="#F59E0B")
        else:
            self.status_label.configure(text="Nothing is currently sending.", text_color="#9CA3AF")

    def on_exit(self):
        if self.sending_thread and self.sending_thread.is_alive():
            if not messagebox.askyesno("Exit", "Emails are still sending. Exit anyway?"):
                return
            self.stop_event.set()
        self.destroy()

    # -------------------- CALLBACKS FROM BACKEND THREAD --------------------
    def _on_progress(self, sent, total):
        # Called from the worker thread -> marshal to GUI thread safely
        self.after(0, self._update_progress_ui, sent, total)

    def _update_progress_ui(self, sent, total):
        self.progress_bar.set(sent / total)
        self.counter_label.configure(text=f"{sent}/{total} Emails Sent")

    def _on_done(self, success, error, was_stopped):
        self.after(0, self._finish_ui, success, error, was_stopped)

    def _finish_ui(self, success, error, was_stopped):
        self.send_btn.configure(state="normal")
        if success and was_stopped:
            self.status_label.configure(text="Stopped by user.", text_color="#F59E0B")
            messagebox.showinfo("Stopped", "Email sending was stopped.")
        elif success:
            self.status_label.configure(text="All emails sent successfully!", text_color="#22C55E")
            messagebox.showinfo("Success", "✅ All emails were sent successfully!")
        else:
            self.status_label.configure(text="An error occurred.", text_color="#EF4444")
            messagebox.showerror("Error", f"❌ Failed to send email(s):\n\n{error}")


if __name__ == "__main__":
    app = EmailSenderApp()
    app.mainloop()
