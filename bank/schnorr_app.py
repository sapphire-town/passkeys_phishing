import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser  # Import the webbrowser module for redirection
import random
import time

class SchnorrSignatureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schnorr Signature System")
        
        # Constants
        self.p = 1019  # Prime modulus
        self.g = 2     # Generator
        
        # Instance variables
        self.public_key = None
        self.private_key = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=5, expand=True, fill='both')
        
        # Registration tab
        reg_frame = ttk.Frame(notebook)
        notebook.add(reg_frame, text='Registration')
        self.setup_registration_frame(reg_frame)
        
        # Signing tab
        sign_frame = ttk.Frame(notebook)
        notebook.add(sign_frame, text='Sign Message')
        self.setup_signing_frame(sign_frame)
        
        # Verification tab
        verify_frame = ttk.Frame(notebook)
        notebook.add(verify_frame, text='Verify Signature')
        self.setup_verification_frame(verify_frame)
        
        # Log frame
        self.log_frame = ttk.Frame(self.root)
        self.log_frame.pack(padx=10, pady=5, expand=True, fill='both')
        self.setup_log_frame()

        # Redirect button
        redirect_button = ttk.Button(self.root, text="Go to Home Page", command=self.redirect_to_home)
        redirect_button.pack(pady=10)

    def setup_registration_frame(self, parent):
        # Passkey entry
        ttk.Label(parent, text="Enter Passkey:").pack(pady=5)
        self.passkey_entry = ttk.Entry(parent, width=40)
        self.passkey_entry.pack(pady=5)
        
        # Register button
        ttk.Button(parent, text="Register", command=self.register).pack(pady=10)
        
        # Public key display
        ttk.Label(parent, text="Public Key:").pack(pady=5)
        self.public_key_label = ttk.Label(parent, text="Not generated")
        self.public_key_label.pack(pady=5)

    def setup_signing_frame(self, parent):
        # Message entry
        ttk.Label(parent, text="Enter Message:").pack(pady=5)
        self.message_entry = ttk.Entry(parent, width=40)
        self.message_entry.pack(pady=5)
        
        # Sign button
        ttk.Button(parent, text="Sign Message", command=self.sign_message).pack(pady=10)
        
        # Signature display
        ttk.Label(parent, text="Signature (r, s):").pack(pady=5)
        self.signature_label = ttk.Label(parent, text="Not generated")
        self.signature_label.pack(pady=5)

    def setup_verification_frame(self, parent):
        # Public key entry
        ttk.Label(parent, text="Enter Public Key:").pack(pady=5)
        self.verify_pubkey_entry = ttk.Entry(parent, width=40)
        self.verify_pubkey_entry.pack(pady=5)
        
        # Signature components entry
        ttk.Label(parent, text="Enter r:").pack(pady=5)
        self.r_entry = ttk.Entry(parent, width=40)
        self.r_entry.pack(pady=5)
        
        ttk.Label(parent, text="Enter s:").pack(pady=5)
        self.s_entry = ttk.Entry(parent, width=40)
        self.s_entry.pack(pady=5)
        
        # Message entry for verification
        ttk.Label(parent, text="Enter Message:").pack(pady=5)
        self.verify_message_entry = ttk.Entry(parent, width=40)
        self.verify_message_entry.pack(pady=5)
        
        # Verify button
        ttk.Button(parent, text="Verify Signature", command=self.verify_signature).pack(pady=10)

    def setup_log_frame(self):
        # Log display
        ttk.Label(self.log_frame, text="Activity Log:").pack(pady=5)
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=10, width=60)
        self.log_text.pack(pady=5)

    def redirect_to_home(self):
        """Redirect to the HTML home page"""
        # Specify the local file path or hosted URL
        url = "http://127.0.0.1:8000/home/"  # Replace with "http://127.0.0.1:5000" if using Flask server
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the webpage: {e}")

    def mod_exp(self, base, exp, mod):
        """Modular exponentiation: (base^exp) % mod"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result

    def hash_function(self, input_str):
        """Simple hash function (sum of ASCII values modulo p)"""
        hash_val = 0
        for c in input_str:
            hash_val = (hash_val + ord(c)) % self.p
        return hash_val

    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f'[{timestamp}] {message}\n')
        self.log_text.see(tk.END)

    def register(self):
        """Handle registration process"""
        passkey = self.passkey_entry.get()
        if not passkey:
            messagebox.showerror("Error", "Please enter a passkey")
            return
        
        self.private_key = self.hash_function(passkey)
        self.public_key = self.mod_exp(self.g, self.private_key, self.p)
        
        self.public_key_label.config(text=str(self.public_key))
        self.log_message(f"Registered with public key: {self.public_key}")

    def sign_message(self):
        """Handle message signing process"""
        if not self.private_key:
            messagebox.showerror("Error", "Please register first")
            return
            
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        # Generate signature
        k = random.randint(1, self.p - 2)
        r = self.mod_exp(self.g, k, self.p)
        e = self.hash_function(message + str(r))
        s = (k + self.private_key * e) % (self.p - 1)
        
        self.signature_label.config(text=f"({r}, {s})")
        self.log_message(f"Signed message: {message}")
        self.log_message(f"Signature: (r={r}, s={s})")

    def verify_signature(self):
        """Handle signature verification process"""
        try:
            y = int(self.verify_pubkey_entry.get())
            r = int(self.r_entry.get())
            s = int(self.s_entry.get())
            message = self.verify_message_entry.get()
            
            if not all([y, r, s, message]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            # Verify signature
            r_prime = (self.mod_exp(self.g, s, self.p) * 
                      self.mod_exp(y, self.p - 1 - self.hash_function(message + str(r)), self.p)) % self.p
            e_prime = self.hash_function(message + str(r_prime))
            e = self.hash_function(message + str(r))
            
            if e == e_prime:
                self.log_message("Signature verification: VALID")
                messagebox.showinfo("Success", "Signature is valid!")
            else:
                self.log_message("Signature verification: INVALID")
                messagebox.showerror("Error", "Invalid signature")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid input format")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchnorrSignatureGUI(root)
    root.mainloop()
