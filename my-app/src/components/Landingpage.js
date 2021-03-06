import React,{Component} from 'react';
import { Redirect } from 'react-router-dom'

import {Link} from 'react-router-dom';
import '../App.css';


const emailRegex = RegExp(
    /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
  );
  
  const formValid = ({ formErrors, ...rest }) => {
    let valid = true;
  
    // validate form errors being empty
    Object.values(formErrors).forEach(val => {
      val.length > 0 && (valid = false);
    });
  
    // validate the form was filled out
    Object.values(rest).forEach(val => {
      val === null && (valid = false);
    });
  
    return valid;
  };
 
  const headers = new Headers({
    Accept: "application/json",
    "Content-Type": "application/json"
});
  


class LandingPage extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          is_Auth: false,
          firstName: null,
          lastName: null,
          email: null,
          password: null,
          confirmpassword: null,
          formErrors: {
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            confirmpassword: "",
            dob:""
          }
        };
      }
    
      testBackend = async () => {

        var user = {
          email: this.state.email,
          name: this.state.firstName + " " + this.state.lastName,
          date: this.state.dob,
          password: this.state.password     
          };
        var users = [user]

        const test = await fetch("http://localhost:8000/patient_signup/", {
          method: "POST",
          headers: headers,
          body: JSON.stringify(users),
          cache: "default"
        });
        const testJson = await test.json();
        if(testJson)
          console.log(testJson.status)
        if(testJson.status == "Ok"){
          alert("Ok");
          this.setState({is_Auth:true});
        }
        else
          alert(((testJson.status[0]).email)[0])  
      }

      handleSubmit = e => {
        e.preventDefault();
    
        if (formValid(this.state)) {
          console.log(`
            --SUBMITTING--
            First Name: ${this.state.firstName}
            Last Name: ${this.state.lastName}
            Email: ${this.state.email}
            Password: ${this.state.password}
            
            Date of Birth: ${this.state.dob}
          `);
          (this.testBackend());
          
        
        } else {
          console.error("FORM INVALID - DISPLAY ERROR MESSAGE");
          alert("Please fulfill all the criteria of each field")
        }
      };
    
      handleChange = e => {
        e.preventDefault();
        const { name, value } = e.target;
        let formErrors = { ...this.state.formErrors };
    
        switch (name) {
          case "firstName":
            formErrors.firstName =
              value.length < 3 ? "minimum 3 characaters required" : "";
            break;
          case "lastName":
            formErrors.lastName =
              value.length < 3 ? "minimum 3 characaters required" : "";
            break;
          case "email":
            formErrors.email = emailRegex.test(value)
              ? ""
              : "invalid email address";
            break;
          case "password":
            formErrors.password =
              value.length < 6 ? "minimum 6 characaters required" : "";
            break;
          case "confirmpassword":
            formErrors.confirmpassword =
              this.state.password!==value?"Entered value dosen't match the original Password":"";
            break;
        case "dob":
            formErrors.dob =
              value.length < 4 ? "minimum 4 characaters required" : "";
            break;
          default:
            break;
        }
    
        this.setState({ formErrors, [name]: value }, () => console.log(this.state));
      };

  
     
    render(){
        const { formErrors } = this.state;
        if(!this.state.is_Auth){
        return(
          <div className="wrapper">
            <div className="form-wrapper">
              <h1>Create Account</h1>
              <form onSubmit={this.handleSubmit} noValidate>
                <div className="firstName">
                  <label htmlFor="firstName">First Name</label>
                  <input
                    className={formErrors.firstName.length > 0 ? "error" : null}
                    placeholder="First Name"
                    type="text"
                    name="firstName"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.firstName.length > 0 && (
                    <span className="errorMessage">{formErrors.firstName}</span>
                  )}
                </div>
                <div className="lastName">
                  <label htmlFor="lastName">Last Name</label>
                  <input
                    className={formErrors.lastName.length > 0 ? "error" : null}
                    placeholder="Last Name"
                    type="text"
                    name="lastName"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.lastName.length > 0 && (
                    <span className="errorMessage">{formErrors.lastName}</span>
                  )}
                </div>
                <div className="email">
                  <label htmlFor="email">Email</label>
                  <input
                    className={formErrors.email.length > 0 ? "error" : null}
                    placeholder="Email"
                    type="email"
                    name="email"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.email.length > 0 && (
                    <span className="errorMessage">{formErrors.email}</span>
                  )}
                </div>
                <div className="dob">
                  <label htmlFor="dob">Date of Birth</label>
                  <input
                    className={formErrors.dob.length > 0 ? "error" : null}
                    placeholder="DD/MM/YYYY"
                    type="date"
                    name="dob"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.dob.length > 0 && (
                    <span className="errorMessage">{formErrors.password}</span>
                  )}
                </div>
                <div className="password">
                  <label htmlFor="password">Password</label>
                  <input
                    className={formErrors.password.length > 0 ? "error" : null}
                    placeholder="Password"
                    type="password"
                    name="password"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.password.length > 0 && (
                    <span className="errorMessage">{formErrors.password}</span>
                  )}
                </div>
                <div className="confirmpassword">
                  <label htmlFor="confirmpassword">Confirm Password</label>
                  <input
                    className={formErrors.confirmpassword.length > 0 ? "error" : null}
                    placeholder="Confirm Password"
                    type="password"
                    name="confirmpassword"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.confirmpassword.length > 0 && (
                    <span className="errorMessage">{formErrors.confirmpassword}</span>
                  )}
                </div>
                <div className="createAccount">
                  <button type="submit">Create Account</button>
                    
                  <Link to ="/doctorsignup"><short>
                  Are you a specialist? Sign up here.
                  </short></Link>  
                
                </div>
              </form>
            </div>
            </div>
            
        )
    }

    else{
      return <Redirect to="/"/>
    }

  }

 
}

export default LandingPage;